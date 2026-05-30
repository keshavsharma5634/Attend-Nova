from src.database.config import supabase
import bcrypt
import streamlit as st 
import time


def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

def check_pass(pwd, hashed):
    return bcrypt.checkpw(pwd.encode(), hashed.encode())


def check_teacher_exists(username):
    # Check for unique username, returns false when username is already taken
    with st.spinner("🔍 Checking username availability..."):
        response = supabase.table("teachers").select("username").eq("username", username).execute()
    return len(response.data) > 0 


def create_teacher(username, password, name):
    with st.spinner("📝 Registering teacher profile..."):
        data = { "username" : username, "password": hash_pass(password), "name": name}
        response = supabase.table("teachers").insert(data).execute()
    return response.data


def teacher_login(username, password):
    with st.spinner("🔐 Authenticating credentials..."):
        response = supabase.table("teachers").select("*").eq("username", username).execute()
    if response.data:
        teacher = response.data[0]
        if check_pass(password, teacher['password']):
            return teacher
    return None


def get_all_students():
    max_retries = 3
    for i in range(max_retries):
        try:
            with st.spinner("👥 Fetching student registry..."):
                response = supabase.table('students').select("*").execute()
            return response.data
        except Exception as e:
            if i < max_retries - 1:
                time.sleep(1)
                continue
            else:
                st.toast("Network slow, please try again.")
                return []

def create_student(new_name, face_embedding=None, voice_embedding=None):
    with st.spinner("➕ Creating student profile..."):
        data = {'name': new_name, 'face_embedding':face_embedding, "voice_embedding": voice_embedding}
        response = supabase.table('students').insert(data).execute()
    return response.data


def create_subject(subject_code, name, section, teacher_id):
    with st.spinner("📚 Creating new subject..."):
        data = {"subject_code": subject_code, "name": name, "section": section, "teacher_id": teacher_id}
        response = supabase.table("subjects").insert(data).execute()
    return response.data


# show_spinner ko True kiya taaki background cache refresh pr spinner dikhe
def get_teacher_subjects(teacher_id):
    response = (
        supabase
        .table("subjects")
        .select(
            "*, subject_students(count), attendance_logs(timestamp)"
        )
        .eq("teacher_id", teacher_id)
        .execute()
    )

    subjects = response.data

    if subjects:
        for sub in subjects:
            student_data = sub.get("subject_students", [])
            sub["total_students"] = (
                student_data[0].get("count", 0)
                if student_data
                else 0
            )

            attendance = sub.get("attendance_logs", [])

            unique_sessions = (
                len(set(log["timestamp"] for log in attendance))
                if attendance
                else 0
            )

            sub["total_classes"] = unique_sessions

            # Cleanup
            sub.pop("subject_students", None)
            sub.pop("attendance_logs", None)

    return subjects


def enroll_student_to_subject(student_id, subject_id):
    with st.spinner("✍️ Enrolling student to subject..."):
        data = {'student_id': student_id, "subject_id": subject_id}
        response = supabase.table('subject_students').insert(data).execute()
    return response.data


def unenroll_student_to_subject(student_id, subject_id):
    with st.spinner("🗑️ Unenrolling student..."):
        response = supabase.table('subject_students').delete().eq('student_id', student_id).eq('subject_id', subject_id).execute()
    return response.data


def get_student_subjects(student_id):
    with st.spinner("📖 Loading student subjects..."):
        response = supabase.table('subject_students').select('*, subjects(*)').eq('student_id', student_id).execute()
    return response.data

def get_student_attendance(student_id):
    with st.spinner("📊 Fetching attendance history..."):
        response = (
            supabase
            .table('attendance_logs')
            .select('*, subjects(*)')
            .eq('student_id', student_id)
            .execute()
        )
    return response.data


# show_spinner ko True kiya taaki record loading spinner automatic trigger ho
@st.cache_data(ttl=30, show_spinner="📊 Syncing attendance records...")
def get_attendance_for_teacher(teacher_id):
    response = supabase.table('attendance_logs')\
        .select("*, subjects!inner(*)")\
        .eq('subjects.teacher_id', teacher_id)\
        .execute()

    return response.data


def create_attendance(logs):
    with st.spinner("💾 Saving logs to database..."):
        response = supabase.table('attendance_logs').insert(logs).execute()
    return response.data