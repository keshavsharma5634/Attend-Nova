import streamlit as st


def footer_home():
    st.markdown("""
        <div style="
            margin-top: 3.5rem;
            padding: 20px 0;
            width: 100%;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            text-align: center !important;
        ">
            <p style="
                font-size: clamp(14px, 4vw, 18px);
                font-weight: 600;
                color: #64748B;
                margin: 0;
                font-family: 'Poppins', system-ui, -apple-system, sans-serif;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                flex-wrap: wrap;
                gap: 6px;
                width: 100%;
            ">
                Created with <span style="color: #ef4444; display: inline;">❤️</span> by
                <span style="
                    color: #2563EB;
                    font-weight: 900;
                    letter-spacing: 0.5px;
                    text-transform: uppercase;
                    display: inline-block;
                ">
                    Keshav Sharma
                </span>
            </p>
        </div>
    """, unsafe_allow_html=True)


def footer_dashboard():
    st.markdown("""
        <div style="
            margin-top: 3rem;
            padding: 16px 0;
            width: 100%;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            text-align: center !important;
        ">
            <p style="
                font-size: clamp(13px, 3.5vw, 16px);
                font-weight: 600;
                color: #475569;
                margin: 0;
                font-family: 'Poppins', system-ui, -apple-system, sans-serif;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                flex-wrap: wrap;
                gap: 6px;
                width: 100%;
            ">
                Created with <span style="color: #ef4444; display: inline;">❤️</span> by
                <span style="
                    color: #2563EB;
                    font-weight: 900;
                    letter-spacing: 0.5px;
                    text-transform: uppercase;
                    display: inline-block;
                ">
                    Keshav Sharma
                </span>
            </p>
        </div>
    """, unsafe_allow_html=True)