import streamlit as st
from utils import check_login
from models import get_messages_for_user

# Enforce authentication
check_login()

st.title("📥 Inbox & Messages")

# Header and refresh button layout
col1, col2 = st.columns([3, 1])
with col1:
    st.write("View your message history.")
with col2:
    if st.button("🔄 Refresh Messages", use_container_width=True):
        st.rerun()

st.divider()

# Organize using tabs
tab1, tab2 = st.tabs(["Received Messages", "Sent Messages"])

current_user_id = st.session_state.user_id

with tab1:
    received = get_messages_for_user(current_user_id, role="receiver")
    if not received:
        st.info("Your inbox is empty.")
    else:
        for msg in received:
            # chat_message UI for left-aligned received messages
            with st.chat_message("user"):
                st.markdown(f"**From {msg['other_person']}** • _{msg['timestamp']}_")
                st.write(msg['content'])

with tab2:
    sent = get_messages_for_user(current_user_id, role="sender")
    if not sent:
        st.info("You haven't sent any messages yet.")
    else:
        for msg in sent:
            # chat_message UI with 'assistant' role for right/different styling
            with st.chat_message("assistant"):
                st.markdown(f"**To {msg['other_person']}** • _{msg['timestamp']}_")
                st.write(msg['content'])\
