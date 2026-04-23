import streamlit as st
from models import get_user_by_email, create_user
from utils import hash_password

def render_login():
    """Renders the login UI and handles authentication logic."""
    st.subheader("Login to your Account")
    
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            user = get_user_by_email(email)
            if user and user['password'] == hash_password(password):
                st.session_state.user_id = user['id']
                st.session_state.user_name = user['name']
                st.success("Login successful! Redirecting...")
                st.rerun() 
            else:
                st.error("Invalid email or password")

def render_register():
    """Renders the registration UI and handles account creation."""
    st.subheader("Create a New Account")
    
    with st.form("register_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submitted = st.form_submit_button("Register")
        
        if submitted:
            if password != confirm_password:
                st.error("Passwords do not match!")
            elif len(password) < 4:
                st.error("Password must be at least 4 characters.")
            else:
                success = create_user(name, email, hash_password(password))
                if success:
                    st.success("Registration successful! Please log in.")
                else:
                    st.error("Email already exists. Try logging in.")