import base64
import os
import streamlit as st


def get_base64_image(image_name):
    # header.py jahan hai (src/components/), uske base par pure project ka root path nikalenge
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Agar file src/components/ ke andar hai, toh ek step piche jaakar src/images/logo.png banayenge
    # Agar directly app.py ke sath root par project run ho raha hai, dono cases handle ho jayenge
    possible_paths = [
        os.path.join(os.path.dirname(current_dir), "images", image_name),  # From src/components/ to src/images/
        os.path.join(current_dir, "src", "images", image_name),  # From root to src/images/
        os.path.join(current_dir, "images", image_name),  # In case it's in src/images/
    ]

    image_path = None
    for path in possible_paths:
        if os.path.exists(path):
            image_path = path
            break

    if image_path and os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return f"data:image/png;base64,{base64.b64encode(img_file.read()).decode()}"
    return ""


def header_home():
    logo_base64 = get_base64_image("logo.png")
    st.markdown(
        f"""
        <div style="
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 12px;
            text-align: center;
            width: 100%;
        ">
            <img src="{logo_base64}" style="width: 150px; height: 150px; border-radius: 25%; object-fit: cover; filter: drop-shadow(0 10px 20px rgba(15,23,42,0.1));">
            <h1 style="
                margin: 0;
                padding: 0;
                font-size: 2.5rem;
                font-weight: 900;
                letter-spacing: 1px;
                background: linear-gradient(135deg, #0f172a 40%, #2563eb 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                line-height: 1.1;
            ">
                AttendNova
            </h1>
        </div>
    """,
        unsafe_allow_html=True,
    )


def header_dashboard():
    logo_base64 = get_base64_image("logo.png")
    st.markdown(
        f"""
        <div style="
            display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: flex-start;
            gap: 16px;
            width: 100%; /* Width 100% rakho, taaki flex container apne parent column ke hisab se adjust ho */
            min-width: 200px;
        ">
            <img src="{logo_base64}" style="width: 85px; height: 85px; border-radius: 25%; object-fit: cover; filter: drop-shadow(0 6px 12px rgba(15,23,42,0.06)); flex-shrink: 0;">
            <h2 style="
                margin: 0;
                padding: 0;
                font-size: 1.9rem;
                font-weight: 900;
                letter-spacing: 1px;
                background: linear-gradient(135deg, #0f172a 50%, #2563eb 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                line-height: 1;
                white-space: nowrap;
                display: block;
            ">
                AttendNova
            </h2>
        </div>
    """,
        unsafe_allow_html=True,
    )
