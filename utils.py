import hashlib
import streamlit as st

# Predefined skills to enforce standard tags
PREDEFINED_SKILLS = [
    "Python", "JavaScript", "Java", "C++", "React", "Node.js", 
    "Web Design", "UI/UX", "Graphic Design", "Video Editing", 
    "Marketing", "SEO", "Copywriting", "Data Science", 
    "Machine Learning", "Mathematics", "Language Tutoring", "Music"
]

def hash_password(password: str) -> str:
    """Hashes a password using SHA-256 for secure storage."""
    return hashlib.sha256(password.encode()).hexdigest()

def format_stars(rating: float) -> str:
    """Converts a float rating (1-5) into a visual star string."""
    if rating is None or rating == 0:
        return "No ratings yet"
    stars = int(round(rating))
    return "⭐" * stars + "☆" * (5 - stars)

def check_login():
    """Checks if the user is authenticated. If not, stops execution and prompts login."""
    if 'user_id' not in st.session_state or st.session_state.user_id is None:
        st.warning("Please log in from the main app page to access this feature.")
        st.stop() 
    else:
        st.sidebar.write(f"Logged in as: **{st.session_state.user_name}**")
        if st.sidebar.button("Logout", key="logout_btn"):
            st.session_state.user_id = None
            st.session_state.user_name = None
            st.switch_page("app.py")