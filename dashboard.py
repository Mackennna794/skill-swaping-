import streamlit as st
from utils import check_login, PREDEFINED_SKILLS, format_stars
from models import get_all_other_users, get_user_rating, send_message, add_review

# Enforce authentication
check_login()

st.title("🌐 Skill Swap Dashboard")
st.write("Discover users and exchange skills!")

# --- FILTERS ---
st.markdown("### Filter Users")
col1, col2 = st.columns(2)
with col1:
    filter_offered = st.selectbox("Looking for someone who offers:", ["All"] + PREDEFINED_SKILLS)
with col2:
    filter_wanted = st.selectbox("Looking for someone who wants:", ["All"] + PREDEFINED_SKILLS)

st.divider()

# --- USER LISTING ---
current_user_id = st.session_state.user_id
all_users = get_all_other_users(current_user_id)

# Filter logic
filtered_users = []
for u in all_users:
    u_offered = u['skills_offered'] if u['skills_offered'] else ""
    u_wanted = u['skills_wanted'] if u['skills_wanted'] else ""
    
    match_offered = filter_offered == "All" or filter_offered in u_offered
    match_wanted = filter_wanted == "All" or filter_wanted in u_wanted
    
    if match_offered and match_wanted:
        filtered_users.append(u)

if not filtered_users:
    st.info("No users match your filter criteria. Try broadening your search.")

# Display user cards
for user in filtered_users:
    rating = get_user_rating(user['id'])
    
    # Card container
    with st.container(border=True):
        c1, c2 = st.columns([2.5, 1.5])
        with c1:
            st.subheader(user['name'])
            st.write(f"**Rating:** {format_stars(rating)} ({rating:.1f}/5)")
            st.write("**Status:** Active recently")
            st.write(f"**Bio:** {user['bio'] if user['bio'] else 'No bio provided.'}")
            
            st.markdown(f"**Offers:** `{user['skills_offered'] if user['skills_offered'] else 'None'}`")
            st.markdown(f"**Wants:** `{user['skills_wanted'] if user['skills_wanted'] else 'None'}`")
            
        with c2:
            # Action Expanders
            with st.expander("📬 Message"):
                msg_content = st.text_area("Write a message", key=f"msg_{user['id']}")
                if st.button("Send", key=f"btn_{user['id']}", use_container_width=True):
                    if not msg_content.strip():
                        st.error("Cannot send empty message.")
                    else:
                        success = send_message(current_user_id, user['id'], msg_content)
                        if success:
                            st.success("Message sent!")
                        else:
                            st.error("Spam block: Duplicate message.")
            
            with st.expander("⭐ Review"):
                rev_rating = st.slider("Rating", 1, 5, 5, key=f"rate_{user['id']}")
                rev_comment = st.text_input("Comment", key=f"cmt_{user['id']}")
                if st.button("Submit", key=f"rev_btn_{user['id']}", use_container_width=True):
                    add_review(current_user_id, user['id'], rev_rating, rev_comment)
                    st.success("Review submitted!")
                    st.rerun()