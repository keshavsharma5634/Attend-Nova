import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase
import time


from src.database.db import create_attendance

def show_attendance_result(df, logs):
   
    if "Is Present" not in df.columns:
        df["Is Present"] = df["Status"].apply(lambda x: True if "Present" in x else False)
    
    display_df = df[["Name", "ID", "Source", "Is Present"]]
    
    edited_df = st.data_editor(
        display_df,
        hide_index=True,
        width='stretch',
        disabled=["Name", "ID", "Source"], # Baaki columns safe hain, sirf attendance toggle hoga
        column_config={
            "Is Present": st.column_config.CheckboxColumn(
                "Status (Check for Present)",
                help="Uncheck to remove wrong detection and mark as ABSENT",
                default=False,
            )
        }
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button('Discard', width='stretch'):
            st.session_state.voice_attendance_results = None
            st.session_state.attendance_images = []
            st.rerun()

    with col2:
        if st.button('Confirm & Save', width='stretch', type='primary'):
            try:
                # ─── LIVE EDITED CHECKBOX DATA MAPPED WITH DB LOGS ───
                updated_logs = []
                for log in logs:
                    # edited_df se current student ki uncheck/check status dhoondho
                    student_row = edited_df[edited_df["ID"] == log["student_id"]]
                    if not student_row.empty:
                        # Database log ka exact status vahi hoga jo teacher ne screen pr final kiya h
                        log["is_present"] = bool(student_row.iloc[0]["Is Present"])
                    updated_logs.append(log)

                # ─── DATABASE SAVING PAR SPINNER LAGAYA ───
                with st.spinner("💾 Saving updated attendance to database..."):
                    create_attendance(updated_logs)
                st.toast("Attendance taken successfully! 🎉")
                st.session_state.attendance_images = []
                st.session_state.voice_attendance_results = None
                return  # Dialog instantly close ho jayega seamlessly
            except Exception as e:
                st.error('Sync failed!')



@st.dialog(" ")
def attendance_result_dialog(df, logs):
    # ─── NATIVE DIALOG CLOSE BUTTON STYLING (PERFECT ROUND CIRCLE) ───
    st.html(
        """
        <style>
        /* Streamlit ke original close button ko perfectly round aur red kiya */
        div[data-testid="stDialog"] button[aria-label="Close"] {
            background: #dc2626 !important; /* Proper Red */
            color: white !important;
            border-radius: 50% !important; /* Perfect Round Circle */
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
        }

        /* Hover Effect */
        div[data-testid="stDialog"] button[aria-label="Close"]:hover {
            background-color: #b91c1c !important;
        }

        /* SVG Cross Icon white setting */
        div[data-testid="stDialog"] button[aria-label="Close"] svg {
            fill: white !important;
            color: white !important;
            width: 14px !important;
            height: 14px !important;
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
        '<p class="clean-dialog-title">Attendance Reports</p>',
        unsafe_allow_html=True
    )

    show_attendance_result(df, logs)