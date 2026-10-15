import streamlit as st
from core import init_db, add_document, list_documents, delete_document

st.set_page_config(page_title="Knowledge Library", page_icon="📚", layout="wide")
init_db()
st.title("📚 Knowledge Library")
st.write("Upload your personal learning documents. Relevant passages can be included in AI Chat answers.")
st.warning("Use documents you are comfortable sending relevant excerpts from to Ollama Cloud. The app stores extracted text locally in the project's data/library folder.")

uploads = st.file_uploader("Choose documents", type=["txt", "md", "pdf", "docx", "py", "json", "csv", "html", "yaml", "yml", "toml", "log"], accept_multiple_files=True)
if uploads and st.button("Add selected files", type="primary"):
    for uploaded in uploads:
        try:
            ok, message = add_document(uploaded.name, uploaded.getvalue())
            (st.success if ok else st.info)(message)
        except Exception as e:
            st.error(f"Could not add {uploaded.name}: {e}")

docs = list_documents()
st.subheader(f"Your documents ({len(docs)})")
if not docs:
    st.info("No documents yet. Upload your learning-profile text files to personalize answers from your own source material.")
else:
    for doc in docs:
        with st.container(border=True):
            col1, col2 = st.columns([5, 1])
            col1.markdown(f"**{doc['filename']}**")
            col1.caption(f"{doc['chars']:,} characters · Added {doc['added_at']}")
            if col2.button("Remove", key=f"remove_{doc['id']}"):
                delete_document(doc['id']); st.rerun()

st.subheader("How retrieval works")
st.write("The starter version ranks text chunks by keyword overlap with your question. It is lightweight and runs locally, but it is not semantic search. You can later upgrade it to embeddings and a vector database if needed.")
