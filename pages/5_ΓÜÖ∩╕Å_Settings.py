import os
import streamlit as st
from core import init_db, list_conversations, list_documents, list_review_items

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")
init_db()
st.title("⚙️ Settings")
st.write("Connect to Ollama Cloud and configure your workspace.")

st.subheader("Ollama Cloud connection")
st.markdown("1. Sign in at [Ollama](https://ollama.com/).\n2. Open your account's API keys page and create a key.\n3. Paste the key below. It is kept in this Streamlit session and is not written to your source files or SQLite database.")
st.warning("The key is sent to Ollama Cloud when you chat. Do not share your key or commit it to Git.")
current = st.session_state.get("ollama_api_key", "")
api_key = st.text_input("Ollama Cloud API key", value=current, type="password", help="Alternatively set OLLAMA_API_KEY in a local .env file.")
model = st.text_input("Default model name", value=st.session_state.get("ollama_model", os.getenv("OLLAMA_MODEL", "gpt-oss:20b")), help="Model availability can vary. Use a model shown as available to your Ollama Cloud account.")
if st.button("Save connection settings", type="primary"):
    st.session_state.ollama_api_key = api_key.strip()
    st.session_state.ollama_model = model.strip()
    st.success("Saved for this running app session.")

if st.button("Test Ollama Cloud connection"):
    key = api_key.strip() or current or os.getenv("OLLAMA_API_KEY")
    chosen_model = model.strip()
    if not key: st.error("Enter an API key first.")
    elif not chosen_model: st.error("Enter a model name first.")
    else:
        try:
            from core import chat_completion
            with st.spinner("Testing…"):
                result = chat_completion([{"role": "user", "content": "Reply with exactly: Connection successful."}], chosen_model, api_key=key, temperature=0)
            st.session_state.ollama_api_key = key
            st.session_state.ollama_model = chosen_model
            st.success("Ollama Cloud responded.")
            st.code(result)
        except Exception as e:
            st.error(f"Connection failed: {e}")
            st.caption("Check the key, model name, internet connection, and whether that model is available to your account.")

st.divider()
st.subheader("Local workspace data")
st.write("Chats, review items, and the document index are stored in `data/workspace.sqlite3`. Extracted document text is stored in `data/library/`. The learning profile is stored in `profile.json`.")
a, b, c = st.columns(3)
a.metric("Chats", len(list_conversations()))
b.metric("Documents", len(list_documents()))
c.metric("Review items", len(list_review_items()))
st.info("Privacy note: document text is stored locally, but relevant retrieved excerpts and your chat messages are sent to Ollama Cloud to generate answers. Avoid uploading sensitive material unless you are comfortable with that.")
