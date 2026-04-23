import streamlit as st
from utils import check_login, PREDEFINED_SKILLS
from models import get_user_by_id, update_user_profile

# Enforce authentication
check_login()

st.title("👤 My Profile")

current_user_id = st.session_state.user_id
user = get_user_by_id(current_user_id)

def parse_skills(skill_str):
    """Safely converts comma-separated DB strings to lists for multiselect."""
    if not skill_str:
        return []
    return [s.strip() for s in skill_str.split(", ") if s.strip() in PREDEFINED_SKILLS]

# Pre-populate form data
current_name = user['name']
current_bio = user['bio'] if user['bio'] else ""
current_offered = parse_skills(user['skills_offered'])
current_wanted = parse_skills(user['skills_wanted'])

st.markdown("Update your profile details below so others can find you.")

with st.form("profile_form"):
    new_name = st.text_input("Full Name", value=current_name)
    new_bio = st.text_area("Bio (Tell people about yourself)", value=current_bio)
    
    # Multiselect ensures clean, standardized data matching the predefined tags
    new_offered = st.multiselect("Skills I Offer", PREDEFINED_SKILLS, default=current_offered)
    new_wanted = st.multiselect("Skills I Want to Learn", PREDEFINED_SKILLS, default=current_wanted)
    
    submit = st.form_submit_button("Update Profile", type="primary")
    
    if submit:
        update_user_profile(current_user_id, new_name, new_bio, new_offered, new_wanted)
        st.session_state.user_name = new_name 
        st.success("Profile updated successfully!")
        st.rerun()