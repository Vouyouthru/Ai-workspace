import os
import streamlit as st
from core import init_db, load_profile, save_profile, list_conversations, create_conversation, get_messages, save_message, delete_conversation, retrieve_context, build_system_prompt, chat_completion, add_review_item

st.set_page_config(page_title="AI Chat", page_icon="💬", layout="wide")
init_db()
st.title("💬 AI Chat")
st.caption("A general-purpose assistant with your profile and relevant library excerpts available as context.")

with st.sidebar:
    st.subheader("Conversations")
    if st.button("＋ New chat", use_container_width=True):
        st.session_state.chat_id = create_conversation()
        st.session_state.chat_messages = []
        st.rerun()
    chats = list_conversations()
    for chat in chats:
        cols = st.columns([5, 1])
        label = chat['title'][:32] + ("…" if len(chat['title']) > 32 else "")
        if cols[0].button(label, key=f"open_{chat['id']}", use_container_width=True):
            st.session_state.chat_id = chat['id']
            st.session_state.chat_messages = [{"role": m['role'], "content": m['content']} for m in get_messages(chat['id'])]
            st.rerun()
        if cols[1].button("×", key=f"delete_{chat['id']}", help="Delete conversation"):
            delete_conversation(chat['id'])
            if st.session_state.get('chat_id') == chat['id']:
                st.session_state.pop('chat_id', None); st.session_state.pop('chat_messages', None)
            st.rerun()
    st.divider()
    model = st.text_input("Ollama Cloud model", value=st.session_state.get("ollama_model", os.getenv("OLLAMA_MODEL", "gpt-oss:20b")), help="Use a model name available to your Ollama Cloud account.")
    st.session_state.ollama_model = model.strip()
    if st.button("Clear current chat from screen"):
        st.session_state.chat_messages = []
        st.rerun()

if "chat_id" not in st.session_state:
    st.session_state.chat_id = create_conversation()
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [{"role": m['role'], "content": m['content']} for m in get_messages(st.session_state.chat_id)]

for i, msg in enumerate(st.session_state.chat_messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and msg["content"].strip():
            if st.button("Save answer for review", key=f"save_answer_{i}"):
                add_review_item(msg["content"][:500], answer=msg["content"], source="AI Chat")
                st.toast("Saved to Progress & Review")

question = st.chat_input("Ask anything…")
if question:
    st.session_state.chat_messages.append({"role": "user", "content": question})
    save_message(st.session_state.chat_id, "user", question)
    with st.chat_message("user"): st.markdown(question)
    with st.chat_message("assistant"):
        try:
            api_key = st.session_state.get("ollama_api_key", "").strip() or None
            profile = load_profile()
            context = retrieve_context(question)
            messages = [{"role": "system", "content": build_system_prompt(profile, context)}]
            # Keep recent conversation turns to control context size.
            for m in st.session_state.chat_messages[-14:]:
                messages.append({"role": m["role"], "content": m["content"]})
            with st.spinner("Thinking with Ollama Cloud…"):
                answer = chat_completion(messages, st.session_state.get("ollama_model", "gpt-oss:20b"), api_key=api_key)
            st.markdown(answer)
            st.session_state.chat_messages.append({"role": "assistant", "content": answer})
            save_message(st.session_state.chat_id, "assistant", answer)
            st.rerun()
        except Exception as e:
            st.error(f"Could not get a response: {e}")
            st.info("Open Settings, add your Ollama Cloud API key, and check that the selected model is available to your account.")
