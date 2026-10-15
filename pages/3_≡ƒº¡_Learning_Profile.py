import streamlit as st
from core import init_db, load_profile, save_profile

st.set_page_config(page_title="Learning Profile", page_icon="🧭", layout="wide")
init_db()
st.title("🧭 Learning Profile")
st.write("This profile guides personalization. Edit anything that feels inaccurate; your learning-style quiz is a hint, not a fixed identity.")
p = load_profile()
with st.form("profile_form"):
    name = st.text_input("Preferred name (optional)", p.get("name", ""))
    learning_preferences = st.text_area("How I learn", p.get("learning_preferences", ""), height=180)
    teaching_instructions = st.text_area("How the assistant should help", p.get("teaching_instructions", ""), height=180)
    goals = st.text_area("Current goals", p.get("goals", ""), height=100)
    subjects_text = st.text_area("Subjects and interests (one per line)", "\n".join(p.get("subjects", [])), height=140)
    submitted = st.form_submit_button("Save profile", type="primary")
if submitted:
    updated = {"name": name.strip(), "learning_preferences": learning_preferences.strip(), "teaching_instructions": teaching_instructions.strip(), "goals": goals.strip(), "subjects": [x.strip() for x in subjects_text.splitlines() if x.strip()]}
    save_profile(updated)
    st.success("Profile saved. New assistant responses will use these settings.")

st.subheader("Current profile summary")
st.markdown("**Your approach:** Try → Discover → Explain → Apply → Recall later")
st.write("The assistant should support your autonomy: direct answers when requested, practical learning when useful.")
