
import os

import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Load credentials from .env
load_dotenv()

st.set_page_config(
    page_title="AI Learning Roadmap Generator",
    page_icon="🗺️",
    layout="wide",
)

# -----------------------------
# App header
# -----------------------------
st.title("AI Learning Roadmap Generator")
st.write(
    "Generate a personalized learning roadmap based on "
    "your skill level, available time, and learning goals."
)

st.divider()

# -----------------------------
# User inputs
# -----------------------------
with st.form("roadmap_form"):
    field = st.text_input(
        "What do you want to learn?",
        placeholder="e.g. Python, AI, Data Science, Web Development",
    )

    level = st.selectbox(
        "Your current skill level",
        ["Beginner", "Intermediate", "Advanced"],
    )

    duration = st.selectbox(
        "How much time do you have?",
        ["1 month", "3 months", "6 months", "12 months"],
    )

    hours_per_day = st.slider(
        "Hours available per day",
        min_value=1,
        max_value=8,
        value=2,
    )

    goal = st.selectbox(
        "Your learning goal",
        [
            "Build real-world projects",
            "Get a job",
            "Start freelancing",
            "Academic learning",
            "Learn for personal interest",
        ],
    )

    submitted = st.form_submit_button(
        "Generate My Roadmap",
        type="primary",
        use_container_width=True,
    )


# -----------------------------
# Generate roadmap
# -----------------------------
if submitted:
    api_key = os.getenv("GROQ_API_KEY")
    model = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

    if not field.strip():
        st.warning("Please enter the field you want to learn.")

    elif not api_key:
        st.error(
            "GROQ_API_KEY is missing. Add it to your .env file "
            "and restart Streamlit."
        )

    else:
        prompt = f"""
Create a practical and personalized learning roadmap.

USER PROFILE
- Learning field: {field.strip()}
- Current level: {level}
- Available duration: {duration}
- Study hours per day: {hours_per_day}
- Main goal: {goal}

REQUIREMENTS
1. Start from the user's current skill level.
2. Arrange topics in the correct learning order.
3. Divide the roadmap into phases and weeks.
4. Estimate a realistic workload for the available time.
5. Include practical exercises and projects for each phase.
6. Explain what the learner should achieve at each milestone.
7. Include revision and self-assessment.
8. Recommend reputable resources and official documentation.
9. Do not invent URLs or claim that mastery is guaranteed.
10. Separate essential skills from optional advanced topics.

FORMAT
# Personalized Learning Roadmap

## 1. Overview
## 2. Prerequisites
## 3. Learning Phases
## 4. Week-by-Week Study Plan
Use a table with: Week, Topics, Practice, Expected Outcome.
## 5. Practical Projects
## 6. Learning Resources
## 7. Progress Checklist
Use Markdown checkboxes.
## 8. Common Mistakes
## 9. First Seven Days Action Plan

Write in clear, beginner-friendly language.
"""

        try:
            client = Groq(api_key=api_key)

            with st.spinner("Creating your personalized roadmap..."):
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are an expert learning roadmap "
                                "designer and technical mentor. "
                                "Create clear, realistic, actionable "
                                "learning plans."
                            ),
                        },
                        {
                            "role": "user",
                            "content": prompt,
                        },
                    ],
                    temperature=0.4,
                    max_completion_tokens=5000,
                )

                roadmap = (
                    response.choices[0].message.content or ""
                ).strip()

            if roadmap:
                st.session_state["roadmap"] = roadmap
                st.session_state["roadmap_field"] = field.strip()
            else:
                st.error("The AI returned an empty response.")

        except Exception as error:
            st.error(
                f"Could not generate the roadmap: "
                f"{type(error).__name__}: {error}"
            )

# -----------------------------
# Display and download result
# -----------------------------
if st.session_state.get("roadmap"):
    st.divider()

    st.subheader(
        "Your Roadmap: "
        + st.session_state.get("roadmap_field", "Learning Plan")
    )

    st.markdown(st.session_state["roadmap"])

    st.download_button(
        label="Download Roadmap",
        data=st.session_state["roadmap"],
        file_name="learning_roadmap.md",
        mime="text/markdown",
        use_container_width=True,
    )
