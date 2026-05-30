import streamlit as st
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from PIL import Image
import numpy as np
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import get_all_students, create_student, get_student_subjects, get_student_attendance, unenroll_student_to_subject
import time
from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card


def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data["student_id"]

    # ─── SECURE INTERFACE RE-ALIGNMENT CONFIGS ───
    st.markdown(
        """
        <style>
        /* Target base wrapper keys directly through precise block mappings */
        div[data-testid="stColumn"]:has(button[key="logoutbtn"]) {
            min-width: 250px !important; /* Button box area spacing standard clear limit */
        }
        
        div[data-testid="stColumn"] button[key="logoutbtn"] {
            background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 14px !important;
            padding: 0.7rem 2rem !important;
            font-weight: 700 !important;
            font-size: 1.02rem !important;
            box-shadow: 0 10px 25px -5px rgba(79, 70, 229, 0.4) !important;
            transition: all 0.2s ease-in-out !important;
            height: auto !important;
            width: 100% !important;
            white-space: nowrap !important; /* Absolute layout tracking block lock */
        }

        div[data-testid="stColumn"] button[key="logoutbtn"]:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 15px 30px -5px rgba(79, 70, 229, 0.55) !important;
            background: linear-gradient(135deg, #1d4ed8 0%, #4338ca 100%) !important;
            color: white !important;
        }

        .welcome-right-panel-text-fixed {
            margin: 0 0 12px 0 !important;
            font-size: 22px !important;
            font-weight: 400 !important;
            color: #0f172a !important;
            text-align: center !important;
            white-space: nowrap !important;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns([5, 1], vertical_alignment="center")

    with c1:
        header_dashboard()

    with c2:
        if st.button("Logout", type="primary", key="logoutbtn"):
            st.session_state["is_logged_in"] = False
            if "student_data" in st.session_state:
                del st.session_state.student_data
            st.session_state["login_type"] = None
            st.rerun()

    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        </style>
        <div style="text-align:center; margin-top:10px; margin-bottom:30px;">
            <h2 style=" color:#0f172a;
            font-weight:500;
            margin-bottom:6px;
            font-size:20px;
            font-family:'Inter', sans-serif !important;">
                👋 Welcome Back, {student_data["name"]}
            </h2>
            <p style="color:#64748b; font-size:18px; margin:0;">
                Manage your attendance, courses and records
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Symmetrical horizontal spacing mapping row lines
    c3, c4 = st.columns([2, 1], vertical_alignment="center")
    with c3:
        st.header("Your Enrolled Subjects")
    with c4:
        if st.button(
            "Enroll in Subject",
            type="primary",
            use_container_width=True,
            key="enroll_subject_main_dashboard_btn",
        ):
            enroll_dialog()

    st.divider()

    # Secure database interaction layer
    subjects = []
    logs = []
    with st.spinner("Loading your enrolled subjects.."):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                subjects = get_student_subjects(student_id)
                logs = get_student_attendance(student_id)
                break
            except Exception:
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
                else:
                    st.error("Database handshake timed out. Please check your network connection.")
                    if st.button("🔄 Retry Connection"):
                        st.rerun()
                    return

    stats_map = {}
    for log in logs:
        sid = log["subject_id"]
        if sid not in stats_map:
            stats_map[sid] = {"total": 0, "attended": 0}
        stats_map[sid]["total"] += 1
        if log.get("is_present"):
            stats_map[sid]["attended"] += 1

    if subjects:
        cols = st.columns(2)
        for i, sub_node in enumerate(subjects):
            sub = sub_node["subjects"]
            sid = sub["subject_id"]
            stats = stats_map.get(sid, {"total": 0, "attended": 0})

            # Scope locking key parameters using default args in lambda/function
            def create_unenroll_callback(course_id, course_name):
                def unenroll_button():
                    if st.button(
                        "Unenroll from this course",
                        type="tertiary",
                        icon=":material/delete_forever:",
                        key=f"unsub_{course_id}",
                    ):
                        unenroll_student_to_subject(student_id, course_id)
                        st.toast(f"Unenrolled from {course_name} successfully!")
                        time.sleep(0.5)
                        st.rerun()
                return unenroll_button

            with cols[i % 2]:
                subject_card(
                    name=sub["name"],
                    code=sub["subject_code"],
                    section=sub["section"],
                    stats=[
                        ("📅", 'Total', stats["total"]),
                        ("✅", 'Attended', stats["attended"]),
                    ],
                    footer_callback=create_unenroll_callback(sid, sub["name"]),
                )
    else:
        st.info("No enrolled courses detected. Click on 'Enroll in Subject' to start adding classes.")

    footer_dashboard()


def student_screen():
    style_background_dashboard()
    style_base_layout()

    # CSS Block
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"], .stApp { background: #f8fafc !important; }
        
        div[data-testid="stColumn"] button[key="logoutbtn"],
        div[data-testid="stColumn"] button[key="enroll_subject_main_dashboard_btn"] {
            background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%) !important;
            color: white !important;
            border-radius: 14px !important;
            padding: 0.7rem 2rem !important;
            font-weight: 700 !important;
        }

        div[data-testid="stColumn"] button[key="ui_back_btn_fixed"] {
            background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%) !important;
            color: white !important;
            border-radius: 12px !important;
            padding: 0.6rem 2rem !important;
            font-weight: 700 !important;
            float: right !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ─── RELOAD SESSION PERSISTENCE ───
    if st.session_state.get("is_logged_in") and st.session_state.get("student_data"):
        student_dashboard()
        return

    # ─── NAVIGATION ROW ───
    nav_col1, nav_col2 = st.columns([3, 1], vertical_alignment="center")
    with nav_col1:
        header_dashboard()
    with nav_col2:
        if st.button("Back", key="ui_back_btn_fixed", type="primary"):
            st.session_state["login_type"] = None
            st.rerun()

    # --- Face Scanning Logic ---
    st.markdown('<div class="hero"><h1>Login using FaceID</h1></div>', unsafe_allow_html=True)
    
    photo_source = st.camera_input("Position your face in the center")
    
    # Bug Fix: Initialize registration flag safely at the top level
    show_registration = False

    if photo_source:
        img = np.array(Image.open(photo_source))

        with st.spinner("AI is scanning.."):
            detected, all_ids, num_faces = predict_attendance(img)

            if num_faces == 0:
                st.warning("Face not found!")
            elif num_faces > 1:
                st.warning("Multiple faces found")
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    student = next(
                        (s for s in all_students if s["student_id"] == student_id),
                        None,
                    )

                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = "student"
                        st.session_state.student_data = student
                        st.toast(f"Welcome Back {student['name']}")
                        time.sleep(1)
                        st.rerun()
                else:
                    st.info("Face not recognized! You might be a new student!")
                    show_registration = True

    if show_registration:
        with st.container(border=True):
            st.header("Register new Profile")
            new_name = st.text_input("Enter your name", placeholder="E.g. Keshav Sharma")

            st.subheader("Optional : Voice Enrollment")
            st.info("Enroll your for voice only attendance")

            audio_data = None
            try:
                audio_data = st.audio_input("Record a short phrase like 'I am present, My name is Keshav Sharma.'")
            except Exception:
                st.error("Audio Data failed!")

            if st.button("Create Account", type="primary"):
                if new_name:
                    with st.spinner("Creating profile.."):
                        img = np.array(Image.open(photo_source))
                        encodings = get_face_embeddings(img)
                        if encodings:
                            face_emb = encodings[0].tolist()
                            voice_emb = None
                            if audio_data:
                                voice_emb = get_voice_embedding(audio_data.read())

                            response_data = create_student(
                                new_name,
                                face_embedding=face_emb,
                                voice_embedding=voice_emb,
                            )

                            if response_data:
                                train_classifier()
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = "student"
                                st.session_state.student_data = response_data[0]
                                st.toast(f"Profile Created! Hi {new_name}!")
                                time.sleep(1)
                                st.rerun()
                        else:
                            st.error("Couldnt capture your facial features for registration")
                else:
                    st.warning("Please enter your name!")

    footer_dashboard()