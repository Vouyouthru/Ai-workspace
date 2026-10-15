import streamlit as st
from core import init_db, add_review_item, list_review_items, rate_review_item, delete_review_item

st.set_page_config(page_title="Progress & Review", page_icon="🧠", layout="wide")
init_db()
st.title("🧠 Progress & Review")
st.write("Save concepts, questions, and mistakes worth revisiting. Review is optional and lightweight—no rigid timetable.")
with st.expander("＋ Save something to review", expanded=False):
    with st.form("add_review"):
        concept = st.text_input("Concept or question", placeholder="e.g. Why does cross-entropy penalize confident wrong predictions?")
        answer = st.text_area("Answer / explanation (optional)", placeholder="Your own explanation or a short reference answer")
        source = st.text_input("Source (optional)", placeholder="e.g. Deep Learning notes")
        submitted = st.form_submit_button("Save for review")
    if submitted:
        if concept.strip():
            add_review_item(concept, answer, source); st.success("Saved."); st.rerun()
        else: st.error("Enter a concept or question first.")

show_all = st.toggle("Show all items", value=False)
items = list_review_items(due_only=not show_all)
st.subheader("All saved items" if show_all else "Due for review")
if not items:
    st.info("Nothing due right now. Save a concept from here or use 'Save answer for review' in AI Chat.")
for item in items:
    with st.container(border=True):
        st.markdown(f"**{item['concept']}**")
        st.caption(f"Due {item['due_date']} · Interval {item['interval_days']} day(s)" + (f" · Source: {item['source']}" if item['source'] else ""))
        if item['answer']:
            with st.expander("Reveal answer / notes"):
                st.write(item['answer'])
        cols = st.columns([1, 1, 1, 1, 1, 1])
        for col, rating in zip(cols[:4], ["Again", "Hard", "Good", "Easy"]):
            if col.button(rating, key=f"rate_{item['id']}_{rating}"):
                rate_review_item(item['id'], rating); st.rerun()
        if cols[5].button("Delete", key=f"del_{item['id']}"):
            delete_review_item(item['id']); st.rerun()
st.caption("Spacing is intentionally simple: Again = 1 day, Hard = 2× the current interval, Good = 4×, Easy = 7×. This is a starter review scheduler, not a validated learning-science algorithm.")
