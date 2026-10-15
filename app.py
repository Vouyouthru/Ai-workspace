import streamlit as st
from core import init_db, load_profile, list_conversations, list_review_items, list_documents

st.set_page_config(page_title="Personal AI Workspace", page_icon="✦", layout="wide", initial_sidebar_state="expanded")
init_db()
profile = load_profile()

st.title("✦ Personal AI Workspace")
st.write("Your AI assistant, personal knowledge library, and learning workspace — all in one place.")
st.caption("Powered by Ollama Cloud · Your saved workspace data stays in this project's local data folder.")

conversations = list_conversations()
docs = list_documents()
reviews = list_review_items(due_only=True)
a, b, c = st.columns(3)
a.metric("Conversations", len(conversations))
b.metric("Library documents", len(docs))
c.metric("Items due for review", len(reviews))

st.subheader("Start here")
col1, col2 = st.columns(2)
with col1:
    st.markdown("### 💬 Ask your assistant")
    st.write("Ask questions, brainstorm, debug code, or explore a concept.")
    if st.button("Open AI Chat", type="primary", use_container_width=True): st.switch_page("pages/1_💬_AI_Chat.py")
with col2:
    st.markdown("### 📚 Add your knowledge")
    st.write("Upload your learning-profile documents and other notes.")
    if st.button("Open Knowledge Library", use_container_width=True): st.switch_page("pages/2_📚_Knowledge_Library.py")

st.subheader("Your learning preferences")
st.info(profile.get("learning_preferences", "Add your preferences in Learning Profile."))
st.caption("Personalization is a guide, not a box: the assistant should answer general questions normally unless learning support is useful.")

st.subheader("Recent conversations")
if not conversations:
    st.write("No conversations yet. Start one from AI Chat.")
else:
    for item in conversations[:5]:
        with st.container(border=True):
            st.write(f"**{item['title']}**")
            st.caption(f"Updated {item['updated_at']} · {item['message_count']} messages")
