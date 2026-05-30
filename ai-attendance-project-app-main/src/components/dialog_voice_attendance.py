import streamlit as st

from src.pipelines.voice_pipeline import process_bulk_audio

from src.database.config import supabase

import pandas as pd


from src.components.dialog_attendance_results import show_attendance_result
from datetime import datetime

@st.dialog(' ')
def voice_attendance_dialog(selected_subject_id):
    # ─── NATIVE MODAL CLOSE BUTTON CUSTOMIZATION (SAME TO SAME PATTERN) ───
    st.html(
        """
        <style>
        /* Streamlit ke original close button ko perfectly round aur red kiya */
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
        </style>
        """
    )

    # Standard Readable Title Element
    st.markdown(
        '<p class="clean-dialog-title">Voice Attendance</p>',
        unsafe_allow_html=True
    )

    st.write('Record audio of students saying I am present. Then AI will recognize the students')

    audio_data = None

    audio_data = st.audio_input("Record classroom audio")

    if st.button('Analyze Audio', width='stretch', type='primary'):
        if not audio_data:
            st.warning("Please record classroom audio first!")
            return

        with st.spinner('Processing Audio data...'):
            enrolled_res = supabase.table('subject_students').select("*, students(*)").eq('subject_id',selected_subject_id ).execute()
            enrolled_students = enrolled_res.data

            if not enrolled_students:
                st.warning('No students enrolled in this course')
                return
            candidates_dict = {
                s['students']['student_id'] : s['students']['voice_embedding'] 
                for s in enrolled_students if s['students'].get('voice_embedding')
            }

            if not candidates_dict:
                st.error('No enrolled students have voice profiles registered')
                return
            
            audio_bytes = audio_data.read()

            detected_scores = process_bulk_audio(audio_bytes, candidates_dict)

            results, attendance_to_log  = [], []

            current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


            for node in enrolled_students:
                student = node['students']
                score  = detected_scores.get(student['student_id'], 0.0)
                is_present= bool(score>0)

                results.append({
                    "Name": student['name'],
                    "ID": student['student_id'],
                    "Source": score if is_present else "-",
                    "Status": "✅ Present" if is_present else "❌ Absent"
                })

                attendance_to_log.append({
                    'student_id': student['student_id'],
                    'subject_id': selected_subject_id,
                    'timestamp': current_timestamp,
                    'is_present': bool(is_present)
                })
            st.session_state.voice_attendance_results = (pd.DataFrame(results), attendance_to_log)

    if st.session_state.get('voice_attendance_results'):
        st.divider()
        df_results, logs = st.session_state.voice_attendance_results
        show_attendance_result(df_results, logs)