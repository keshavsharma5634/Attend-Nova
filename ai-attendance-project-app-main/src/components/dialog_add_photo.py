import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase
from PIL import Image
import time


@st.dialog(" ")
def add_photos_dialog():
    # ─── RED CIRCLE CLOSE BUTTON OVERRIDE ───
    st.html(
        """
        <style>
        div[data-testid="stDialog"] button[aria-label="Close"] {
            background: #dc2626 !important; /* Perfect Red */
            color: white !important;
            border-radius: 50% !important; /* Perfect Circle */
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

        div[data-testid="stDialog"] button[aria-label="Close"]:hover {
            background-color: #b91c1c !important;
        }

        div[data-testid="stDialog"] button[aria-label="Close"] svg {
            fill: white !important;
            color: white !important;
            width: 14px !important;
            height: 14px !important;
        }

        .clean-dialog-title {
            font-family: sans-serif !important;
            font-size: 1.5rem !important;
            font-weight: 600 !important;
            color: #1e293b !important;
            margin-top: -30px !important;
            margin-bottom: 12px !important;
        }
        </style>
        """
    )
    
    st.markdown('<p class="clean-dialog-title">Capture or upload photos</p>', unsafe_allow_html=True)
    st.write('Add classroom photos to scan for attendance')

    if 'photo_tab' not in st.session_state:
        st.session_state.photo_tab = 'camera'

    t1, t2 = st.columns(2)

    with t1:
        type_camera = "primary" if st.session_state.photo_tab == 'camera' else 'tertiary'
        if st.button('Camera', type=type_camera, width='stretch'):
            st.session_state.photo_tab = 'camera'
            st.rerun()

    with t2:
        type_upload = "primary" if st.session_state.photo_tab == 'upload' else 'tertiary'
        if st.button('Upload photos', type=type_upload, width='stretch'):
            st.session_state.photo_tab = 'upload'
            st.rerun()

    # --- CAMERA INPUT CONTROL ---
    if st.session_state.photo_tab == 'camera':
        cam_photo = st.camera_input('Take Snapshot', key='dialog_cam')
        if cam_photo:
            img = Image.open(cam_photo)
            if img not in st.session_state.attendance_images:
                st.session_state.attendance_images.append(img)
                st.toast('Photo Captured! 📸')

    # --- FILE UPLOADER CONTROL ---
    if st.session_state.photo_tab == 'upload':
        uploaded_files = st.file_uploader('choose image files', type=['jpg', 'png', 'jpeg'], accept_multiple_files=True, key='dialog_upload')

        if uploaded_files:
            new_photos_added = False
            for f in uploaded_files:
                img = Image.open(f)
                if not any(img.size == existing.size for existing in st.session_state.attendance_images):
                    st.session_state.attendance_images.append(img)
                    new_photos_added = True
            
            if new_photos_added:
                st.toast('Photos Uploaded Successfully! 🎉')

    st.divider()
    
    # ─── DONE BUTTON PAR FINALLY SPINNER INTEGRATE KIYA ───
    if st.button('Done', type='primary', width='stretch'):
        with st.spinner("🔄 Updating classroom photos registry..."):
            time.sleep(0.8) # Spinner ko visually hold karne ke liye perfect small delay
        return  # Smooth return jisse dialog instantly dismiss ho jaye bina glitch ke