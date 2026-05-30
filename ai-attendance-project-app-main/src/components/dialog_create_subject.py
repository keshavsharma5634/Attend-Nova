import streamlit as st
from src.database.db import create_subject


@st.dialog(" ")
def create_subject_dialog(teacher_id):
    # ─── NATIVE DIALOG CLOSE BUTTON STYLING (PERFECT ROUND CIRCLE) ───
    st.html(
        """
        <style>
        /* Streamlit ke original close button ko completely shape-lock aur round kiya */
        div[data-testid="stDialog"] button[aria-label="Close"] {
            background: #dc2626 !important; /* Proper Red */
            color: white !important;
            
            /* FORCE ROUND SHAPE SHIELD */
            border-radius: 50% !important; 
            clip-path: circle(50%) !important;
            overflow: hidden !important;
            
            /* STRICT SIZE UNIFORMITY */
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

        /* Font style overriding standard h2 font issues */
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

    # <h2> ki jagah custom class lagayi taaki standard readable font aaye
    st.markdown(
        '<p class="clean-dialog-title">📚 Create New Subject</p>',
        unsafe_allow_html=True
    )

    st.write("Enter the details of new subject")

    sub_id = st.text_input("Subject Code", placeholder="CS101")

    sub_name = st.text_input(
        "Subject Name", placeholder="Introduction to Computer Science"
    )

    sub_section = st.text_input("Section", placeholder="A")

    # Bottom layout action controls
    btn_col1, btn_col2 = st.columns([1, 2])
    
    with btn_col1:
        if st.button("Cancel", width="stretch", key="cancel_dialog_btn"):
            return

    with btn_col2:
        if st.button("Create Subject Now", type="primary", width="stretch"):
            if sub_id and sub_name and sub_section:
                try:
                    with st.spinner("📚 Creating subject..."):
                        create_subject(
                            sub_id, sub_name, sub_section, teacher_id
                        )

                    st.toast("✅ Subject Created Successfully!")
                    return

                except Exception as e:
                    st.error(f"Error: {str(e)}")
            else:
                st.warning("Please fill all the fields")