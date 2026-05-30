import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase
import time


@st.dialog(" ")
def enroll_dialog():
    # ─── NATIVE MODAL CLOSE BUTTON CUSTOMIZATION (SAME TO SAME PATTERN) ───
    st.html(
        """
        <style>
        /* Target dynamic text inputs inside dialog for sharp modern look */
        div[data-testid="stDialog"] input {
            border-radius: 12px !important;
            border: 1px solid #cbd5e1 !important;
        }

        /* Target the native top-right close button container - PERFECT ROUND CIRCLE */
        div[data-testid="stDialog"] button[aria-label="Close"] {
            background: #dc2626 !important; /* Standardized Red */
            color: white !important;
            border-radius: 50% !important;
            clip-path: circle(50%) !important;
            overflow: hidden !important;
            width: 32px !important;
            height: 32px !important;
            min-width: 32px !important;
            max-width: 32px !important;
            min-height: 32px !important;
            max-height: 32px !important;
            padding: 0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            border: none !important;
            box-shadow: 0 2px 8px rgba(220, 38, 38, 0.4) !important;
            position: absolute !important;
            right: 20px !important;
            top: 20px !important;
            z-index: 999999 !important;
            line-height: 0 !important;
            transition: background-color 0.2s ease !important;
        }

        div[data-testid="stDialog"] button[aria-label="Close"]:hover {
            background-color: #b91c1c !important;
        }

        /* SVG Cross Icon to White setting */
        div[data-testid="stDialog"] button[aria-label="Close"] svg {
            fill: white !important;
            color: white !important;
            width: 14px !important;
            height: 14px !important;
            display: block !important;
        }

        /* Clean System Font Header Styling */
        .clean-dialog-title {
            font-family: "Source Sans Pro", -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif !important;
            font-size: 1.5rem !important;
            font-weight: 600 !important;
            color: #1e293b !important;
            margin-top: -30px !important;
            margin-bottom: 12px !important;
            letter-spacing: normal !important;
            text-transform: none !important;
        }

        /* Primary action theme synchronization */
        div[data-testid="stDialog"] button[type="primary"] {
            background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 14px !important;
            padding: 0.7rem 2rem !important;
            font-weight: 700 !important;
            font-size: 1.02rem !important;
            box-shadow: 0 8px 20px -5px rgba(79, 70, 229, 0.4) !important;
            transition: all 0.2s ease-in-out !important;
        }

        div[data-testid="stDialog"] button[type="primary"]:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 12px 25px -5px rgba(79, 70, 229, 0.5) !important;
        }
        </style>
        """
    )

    # Standard Readable Title Element
    st.markdown(
        '<p class="clean-dialog-title">Enroll in Subject</p>',
        unsafe_allow_html=True
    )

    # ─── DIALOG DESCRIPTION ───
    st.write('Enter the subject code provided by your teacher to enroll')

    # ─── CONTROL INPUT FIELDS ───
    join_code = st.text_input('Subject Code', placeholder='Eg. CS101')

    # ─── SUBMIT ACTION FLOW ───
    if st.button('Enroll now', type='primary', use_container_width=True):
        if join_code:
            # ─── SUPABASE SE DATA CHECK KARTE WAQT SPINNER LAGAYA ───
            with st.spinner("🔍 Fetching subject details..."):
                res = supabase.table('subjects').select('subject_id, name, subject_code').eq('subject_code', join_code).execute()
            
            if res.data:
                subject = res.data[0]
                student_id = st.session_state.student_data['student_id']

                # ─── ENROLLMENT VERIFY KARTE WAQT SPINNER LAGAYA ───
                with st.spinner("⏳ Checking your enrollment status..."):
                    check = supabase.table('subject_students').select('*').eq('subject_id', subject['subject_id']).eq('student_id', student_id).execute()
                
                if check.data:
                    st.warning('You are already enrolled in this program')
                else:
                    # ─── DATA INSERT (MAIN QUERY) PAR SPINNER LAGAYA ───
                    with st.spinner("✍️ Registering you into the subject..."):
                        enroll_student_to_subject(student_id, subject['subject_id'])
                    
                    st.success('Successfully enrolled! 🎉')
                    time.sleep(1)
                    return  # Native smooth close without jarring page refresh
            else:
                st.error('Invalid subject code. Program not found.')
        else:
            st.warning('Please enter a subject code')