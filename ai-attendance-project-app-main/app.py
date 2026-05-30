import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "src")

for path in [current_dir, src_dir]:
    if path not in sys.path:
        sys.path.insert(0, path)

import streamlit as st

# Imports se 'src.' hata diya taaki direct access ho sake
from screens.home_screen import home_screen
from screens.teacher_screen import teacher_screen
from screens.student_screen import student_screen
from components.dialog_auto_enroll import auto_enroll_dialog

def main():
    st.set_page_config(
        page_title='Attend Nova - Making Attendance faster using AI',
        page_icon="./src/images/logo.png"
    )
    
    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None

    match st.session_state['login_type']:
        case 'teacher':
            teacher_screen()

        case 'student':
            student_screen()
        
        case None:
            home_screen()


    join_code = st.query_params.get('join-code')
    if join_code:
        if st.session_state.login_type != 'student':
            st.session_state.login_type = 'student'
            st.rerun()
        if st.session_state.get('is_logged_in') and st.session_state.get('user_role') == 'student':
            auto_enroll_dialog(join_code)
main()
