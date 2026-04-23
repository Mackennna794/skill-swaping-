import streamlit as st
from database import init_db, get_all_users, get_user_by_id, update_user, get_messages_for_user, send_message
from auth import render_login, render_register

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Skill Swap Platform", page_icon="🔄", layout="centered")

# Initialize database tables on startup
init_db()

# Initialize session state variables
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None

# --- MAIN ROUTING LOGIC ---
if st.session_state.user_id is None:
    st.title("🔄 Welcome to Skill Swap")
    st.write("Exchange skills, learn together, and grow your network!")
    
    # Authentication Tabs
    tab1, tab2 = st.tabs(["Login", "Register"])
    with tab1:
        render_login()
    with tab2:
        render_register()
else:
    # Sidebar Navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "Profile", "Inbox"])
    
    if page == "Dashboard":
        st.title(f"🎯 Dashboard - Welcome, {st.session_state.user_name}!")
        st.write("Find people to swap skills with!")
        
        # Show current user's profile
        current_user = get_user_by_id(st.session_state.user_id)
        st.info(f"📌 **Your Profile:** Offers: {current_user['skills_offered']} | Wants: {current_user['skills_wanted']}")
        
        st.divider()
        st.subheader("👥 Available Users to Connect With")
        
        users = get_all_users()
        other_users = [u for u in users if u['id'] != st.session_state.user_id]
        
        if not other_users:
            st.warning("No other users available yet. Be the first to join!")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("➕ Add Sample Users"):
                    # Add sample users for testing
                    from database import get_connection
                    conn = get_connection()
                    cursor = conn.cursor()
                    sample_users = [
                        ("Alice Smith", "alice@example.com", "hashed_pwd", "JavaScript", "Python", "Love coding!"),
                        ("Bob Johnson", "bob@example.com", "hashed_pwd", "Guitar", "Piano", "Music enthusiast"),
                        ("Carol Davis", "carol@example.com", "hashed_pwd", "Photography", "Painting", "Creative person"),
                    ]
                    for name, email, pwd, offers, wants, bio in sample_users:
                        try:
                            cursor.execute(
                                "INSERT INTO users (name, email, password, skills_offered, skills_wanted, bio) VALUES (?, ?, ?, ?, ?, ?)",
                                (name, email, pwd, offers, wants, bio)
                            )
                        except:
                            pass
                    conn.commit()
                    conn.close()
                    st.success("Sample users added!")
                    st.rerun()
        else:
            for user in other_users:
                with st.container():
                    col1, col2, col3 = st.columns([2, 2, 1])
                    with col1:
                        st.write(f"**{user['name']}**")
                        st.caption(f"📧 {user['email']}")
                    with col2:
                        st.write(f"🎓 Offers: **{user['skills_offered']}**")
                        st.write(f"📚 Wants: **{user['skills_wanted']}**")
                    with col3:
                        if st.button(f"💬 Message", key=f"msg_{user['id']}"):
                            st.session_state.selected_user = user['id']
                            st.rerun()
                    if user['bio']:
                        st.caption(f"Bio: {user['bio']}")
                    st.divider()
        
        # Message form
        if 'selected_user' in st.session_state:
            selected = get_user_by_id(st.session_state.selected_user)
            st.subheader(f"✉️ Message {selected['name']}")
            with st.form("message_form"):
                content = st.text_area("Message")
                submitted = st.form_submit_button("Send Message")
                if submitted and content:
                    send_message(st.session_state.user_id, st.session_state.selected_user, content)
                    st.success("Message sent!")
                    del st.session_state.selected_user
                    st.rerun()
    
    elif page == "Profile":
        st.title("Your Profile")
        user = get_user_by_id(st.session_state.user_id)
        with st.form("profile_form"):
            name = st.text_input("Name", value=user['name'])
            email = st.text_input("Email", value=user['email'])
            skills_offered = st.text_input("Skills Offered", value=user['skills_offered'])
            skills_wanted = st.text_input("Skills Wanted", value=user['skills_wanted'])
            bio = st.text_area("Bio", value=user['bio'])
            submitted = st.form_submit_button("Update Profile")
            if submitted:
                update_user(st.session_state.user_id, name, email, skills_offered, skills_wanted, bio)
                st.session_state.user_name = name
                st.success("Profile updated!")
                st.rerun()
    
    elif page == "Inbox":
        st.title("Inbox")
        messages = get_messages_for_user(st.session_state.user_id)
        if messages:
            for msg in messages:
                st.write(f"From {msg['sender_name']}: {msg['content']} ({msg['timestamp']})")
        else:
            st.write("No messages yet.")