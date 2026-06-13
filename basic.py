import streamlit as st
from gemini_utils import explain_topic, summarize_notes, generate_quiz,generate_study_plan

st.set_page_config(
    page_title="AI-Powered Study Buddy",
    page_icon="📚",
    layout="centered"
)

st.title("📚 AI-Powered Study Buddy")
st.write("Learn smarter with AI ✨")

option = st.selectbox(
    "Choose what you want to do:",
    ["Explain a Topic", "Summarize Notes", "Generate Quiz","Generate Study Plan"]
)

user_input = st.text_area(
    "Enter your topic or notes:",
    height=200,
    placeholder="Example: PN Junction Diode"
)
if option == "Generate Study Plan":
                    subjects = st.text_area(
                    "Enter subjects (comma separated):",
                    placeholder="Maths, Physics, DBMS, Python"
                    )

                    difficulty = st.selectbox(
                    "Overall difficulty level:",
                    ["Easy", "Medium", "Hard"]
                    )

                    days = st.number_input(
                    "Number of available study days:",
                    min_value=1,
                    max_value=60,
                    value=7
                    )

if st.button("Generate ✨"):
    if user_input.strip() == "":
        st.warning("Please enter some text.")
    else:
        with st.spinner("AI is thinking 🧠..."):
            if option == "Explain a Topic":
                output = explain_topic(user_input)
            elif option == "Summarize Notes":
                output = summarize_notes(user_input)
            elif option == "Generate Study Plan":
                output = generate_study_plan(subjects, difficulty, days)
            else:
                output = generate_quiz(user_input)

        st.subheader("📌 Output")
        st.code(output)