import streamlit as st
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, style_background_home


def home_screen():
    style_background_home()
    style_base_layout()

    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"], .stApp {
        background: radial-gradient(at 0% 0%, rgba(224, 242, 254, 0.7) 0, transparent 50%),
                    radial-gradient(at 100% 0%, rgba(199, 210, 254, 0.7) 0, transparent 50%),
                    radial-gradient(at 50% 100%, rgba(244, 243, 249, 1) 0, transparent 100%),
                    #f8fafc !important;
    }
    
    [data-testid="stHeader"] {
        background: transparent !important;
    }
    
    .main > div {
        padding-top: 1.5rem !important;
        max-width: 1200px !important;
    }

    .hud-navbar {
        width: 100%;
        padding: 1.25rem 2.5rem;
        margin-bottom: 2.5rem;
        border-radius: 24px;
        background: rgba(255, 255, 255, 0.5) !important;
        backdrop-filter: blur(25px) !important;
        -webkit-backdrop-filter: blur(25px) !important;
        border: 1px solid rgba(255, 255, 255, 0.7) !important;
        box-shadow: 0 16px 40px -10px rgba(15, 23, 42, 0.06) !important;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .brand {
        font-size: 1.9rem !important;
        font-weight: 900 !important;
        color: #0f172a !important;
        letter-spacing: -0.03em;
        font-family: system-ui, -apple-system, sans-serif;
    }

    .brand::shadow, .brand {
        background: linear-gradient(135deg, #0f172a 60%, #2563eb 100%);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
    }

    .nav-status {
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
    }

    .status-pill {
        padding: 8px 16px;
        border-radius: 100px;
        background: rgba(255, 255, 255, 0.85) !important;
        border: 1px solid rgba(226, 232, 240, 0.9) !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        color: #1e293b !important;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03);
    }

    .hero {
        text-align: center;
        padding: 2rem 0 3.5rem 0;
        width: 100% !important;
        box-sizing: border-box !important;
    }

    .hero h1 {
        font-size: clamp(2.2rem, 7vw, 4.5rem) !important;
        font-weight: 900 !important;
        letter-spacing: 1px !important;
        line-height: 1.2 !important;
        background: linear-gradient(135deg, #0f172a 30%, #312e81 100%);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        margin-bottom: 1rem !important;
        word-break: keep-all !important;
        overflow-wrap: break-word !important;
        width: 100% !important;
        display: block !important;
    }

    .hero p {
        font-size: clamp(0.95rem, 3vw, 1.25rem) !important;
        color: #475569 !important;
        max-width: 650px;
        margin: 0 auto !important;
    }

    div[data-testid="stHorizontalBlock"] {
        gap: 2.5rem !important;
    }

    .portal-card {
        padding: 2.5rem 2rem !important;
        border-radius: 32px !important;
        background: rgba(255, 255, 255, 0.65) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.8) !important;
        box-shadow: 0 20px 50px -12px rgba(15, 23, 42, 0.08) !important;
        transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.3s ease !important;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100% !important;
    }

    .portal-card:hover {
        transform: translateY(-6px) scale(1.01) !important;
        box-shadow: 0 30px 60px -15px rgba(99, 102, 241, 0.15) !important;
    }

    .portal-title {
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        color: #0f172a !important;
        margin-top: 1rem !important;
    }

    .portal-desc {
        color: #64748b !important;
        font-size: 1rem !important;
        margin-top: 0.5rem !important;
        line-height: 1.6 !important;
    }

    .features-row {
        display: flex !important;
        flex-direction: row !important;
        justify-content: space-between !important;
        align-items: stretch !important;
        gap: 1.5rem !important;
        width: 100% !important;
        margin-top: 1rem !important;
        flex-wrap: nowrap !important;
    }

    .feature-card {
        background: rgba(255, 255, 255, 0.65) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.8) !important;
        border-radius: 32px !important;
        padding: 1.8rem 1.2rem !important; 
        text-align: center !important;
        flex: 1 !important;
        width: 33.33% !important;
        min-height: 180px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 10px !important;
        transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.3s ease !important;
        box-shadow: 0 20px 50px -12px rgba(15, 23, 42, 0.08) !important;
    }

    .feature-card:hover {
        transform: translateY(-6px) scale(1.01) !important;
        background: rgba(255, 255, 255, 0.8) !important;
        box-shadow: 0 30px 60px -15px rgba(99, 102, 241, 0.15) !important;
    }

    .feature-card h1 {
        font-size: 2.2rem !important;
        margin: 0 !important;
        line-height: 1 !important;
    }

    .feature-card h3 {
        color: #0f172a !important;
        font-weight: 800 !important;
        font-size: clamp(1rem, 2.5vw, 1.35rem) !important;
        margin: 4px 0 2px 0 !important;
        white-space: normal !important;
        width: 100% !important;      
        text-align: center !important;
        overflow-wrap: break-word !important;
        word-break: normal !important;
    }

    .feature-card p {
        color: #64748b !important;
        font-size: clamp(0.8rem, 2vw, 0.95rem) !important;
        margin: 0 !important;
        line-height: 1.4 !important;
        white-space: normal !important;
        width: 100% !important;      
        text-align: center !important;
        overflow-wrap: break-word !important;
    }

    div[data-testid="stButton"] button {
        background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        box-shadow: 0 10px 25px -5px rgba(79, 70, 229, 0.4) !important;
        transition: all 0.2s ease-in-out !important;
        height: auto !important;
        width: 100% !important;
        margin-top: 1rem !important;
    }

    div[data-testid="stButton"] button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 15px 30px -5px rgba(79, 70, 229, 0.55) !important;
        background: linear-gradient(135deg, #1d4ed8 0%, #4338ca 100%) !important;
    }

    .metrics {
        display: flex;
        justify-content: center;
        gap: 1.5rem;
        margin-top: 4rem;
        flex-wrap: wrap;
    }

    .metric-card {
        padding: 1.25rem 2rem;
        border-radius: 24px;
        background: rgba(255, 255, 255, 0.5) !important;
        backdrop-filter: blur(15px) !important;
        border: 1px solid rgba(255, 255, 255, 0.6) !important;
        box-shadow: 0 10px 30px -10px rgba(15, 23, 42, 0.04) !important;
        text-align: center;
        min-width: 220px;
    }

    .metric-value {
        font-size: 1.7rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
    }

    .metric-label {
        color: #64748b !important;
        font-size: 0.9rem !important;
        margin-top: 0.25rem;
    }

    [data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] div {
        text-align: center !important;
        justify-content: center !important;
    }

    @media (max-width: 991px) {
        .features-row {
            flex-wrap: wrap !important;
            justify-content: center !important;
            gap: 1.5rem !important;
        }
        .feature-card {
            width: 100% !important;
            max-width: 100% !important;
            min-height: auto !important;
            padding: 1.5rem 1.2rem !important;
        }
    }

    @media (max-width: 768px) {
        .hud-navbar {
            flex-direction: column !important;
            align-items: center !important;
            gap: 14px !important;
            padding: 1.5rem !important;
        }
        .nav-status {
            justify-content: center !important;
            gap: 8px !important;
        }
        .hero h1 {
            margin-bottom: 0.5rem !important;
        }
        div[data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
            gap: 1.5rem !important;
        }
        .metric-card {
            width: 100% !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="hud-navbar">
        <div class="brand">AttendNova</div>
        <div class="nav-status">
            <div class="status-pill">🔒 Secure</div>
            <div class="status-pill">⚡ Fast</div>
            <div class="status-pill">🎤 Voice</div>
            <div class="status-pill">📷 Face</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="hero">
        <h1>AttendNova</h1>
        <p>Face Recognition • Voice Authentication • Smart Attendance</p>
        <p style="font-size:15px; color:#64748b; margin-top:12px; font-weight:550;">
            Trusted by Modern Classrooms
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
        <div class="portal-card">
            <img src="https://i.ibb.co/844D9Lrt/mascot-student.png"style="height:110px; object-fit:contain;">
            <div class="portal-title">Student Portal</div>
            <div class="portal-desc">
                Quick Face Login<br>
                Attendance History<br>
                Instant Enrollment
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "🎓 Launch Student Portal",
            type="primary",
            use_container_width=True,
            key="student_btn"
        ):
            st.session_state['login_type'] = 'student'
            st.rerun()

    with col2:
        st.markdown("""
        <div class="portal-card">
            <img src="https://i.ibb.co/CsmQQV6X/mascot-prof.png"style="height:110px; object-fit:contain;">
            <div class="portal-title">Teacher <br> Portal</div>
            <div class="portal-desc">
                AI Attendance<br>
                Analytics Dashboard<br>
                Class Management
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "👨‍🏫 Launch Teacher Portal",
            type="primary",
            use_container_width=True,
            key="teacher_btn"
        ):
            st.session_state['login_type'] = 'teacher'
            st.rerun()

    st.markdown("""
    <div class="metrics">
        <div class="metric-card">
            <div class="metric-value">99.8%</div>
            <div class="metric-label">Recognition Accuracy</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">&lt;1s</div>
            <div class="metric-label">Verification Time</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">24/7</div>
            <div class="metric-label">Availability</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-top:55px; margin-bottom:5px; width:100%;">
        <h2 style="text-align:center; color:#0f172a; font-weight:800; font-size:2.1rem; letter-spacing:1px;">Why AttendNova?</h2>
    </div>
    
    <div class="features-row">
        <div class="feature-card">
            <h1>🎯</h1>
            <h3>Face ID</h3>
            <p>Advanced AI identity verification</p>
        </div>
        <div class="feature-card">
            <h1>🎤</h1>
            <h3>Voice ID</h3>
            <p>Hands-free attendance</p>
        </div>
        <div class="feature-card">
            <h1>📊</h1>
            <h3>Smart Analytics</h3>
            <p>Real-time attendance insights</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    footer_home()