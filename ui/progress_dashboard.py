
import streamlit as st
import json
import os
from datetime import datetime


# ==========================================
# STORAGE
# ==========================================

DATA_FOLDER = "data"
PROGRESS_FILE = os.path.join(DATA_FOLDER, "learning_progress.json")

TOPICS = [
    "Arrays",
    "Linked Lists",
    "Stacks",
    "Queues",
    "Binary Trees",
    "Binary Search Trees",
    "Recursion",
    "Searching Algorithms",
    "Sorting Algorithms",
    "Greedy Algorithms",
    "Dynamic Programming",
    "Graph Algorithms"
]


def load_progress():
    os.makedirs(DATA_FOLDER, exist_ok=True)

    if not os.path.exists(PROGRESS_FILE):
        return {
            "completed_topics": [],
            "quiz_history": []
        }

    try:
        with open(PROGRESS_FILE, "r") as file:
            data = json.load(file)

        data.setdefault("completed_topics", [])
        data.setdefault("quiz_history", [])

        return data

    except (json.JSONDecodeError, OSError):
        return {
            "completed_topics": [],
            "quiz_history": []
        }


def save_progress(data):
    os.makedirs(DATA_FOLDER, exist_ok=True)

    with open(PROGRESS_FILE, "w") as file:
        json.dump(data, file, indent=4)


# ==========================================
# ADD QUIZ RESULT
# ==========================================

def record_quiz_result(difficulty, score, total):

    data = load_progress()

    percentage = (score / total * 100) if total else 0

    data["quiz_history"].append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "difficulty": difficulty,
        "score": score,
        "total": total,
        "percentage": round(percentage, 2)
    })

    save_progress(data)


# ==========================================
# MAIN PROGRESS DASHBOARD
# ==========================================

def render_progress_dashboard():

    st.title("📊 Learning Progress Dashboard")

    st.write(
        "Track your DSA learning journey, quiz performance "
        "and completed topics."
    )

    data = load_progress()

    completed = data["completed_topics"]
    history = data["quiz_history"]

    total_topics = len(TOPICS)
    completed_count = len(completed)

    progress = (
        completed_count / total_topics
        if total_topics else 0
    )

    # ======================================
    # OVERVIEW
    # ======================================

    st.subheader("Learning Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Completed Topics",
        f"{completed_count}/{total_topics}"
    )

    col2.metric(
        "Quiz Attempts",
        len(history)
    )

    average = (
        sum(x["percentage"] for x in history) / len(history)
        if history else 0
    )

    col3.metric(
        "Average Accuracy",
        f"{average:.1f}%"
    )

    st.progress(progress)

    st.caption(
        f"Overall topic completion: {progress * 100:.1f}%"
    )

    st.divider()

    # ======================================
    # TOPIC TRACKER
    # ======================================

    st.subheader("📚 DSA Topic Tracker")

    st.write("Mark topics as completed when you finish learning them.")

    selected_topics = st.multiselect(
        "Select completed topics",
        TOPICS,
        default=[
            topic for topic in completed
            if topic in TOPICS
        ],
        key="progress_topic_selection"
    )

    if st.button("Save Topic Progress", type="primary"):

        data["completed_topics"] = selected_topics
        save_progress(data)

        st.success("Learning progress saved!")
        st.rerun()

    for topic in TOPICS:

        if topic in completed:
            st.success(f"✓ {topic}")
        else:
            st.write(f"○ {topic}")

    st.divider()

    # ======================================
    # QUIZ PERFORMANCE
    # ======================================

    st.subheader("🎯 Quiz Performance")

    if history:

        easy = [
            x["percentage"]
            for x in history
            if x["difficulty"] == "Easy"
        ]

        medium = [
            x["percentage"]
            for x in history
            if x["difficulty"] == "Medium"
        ]

        hard = [
            x["percentage"]
            for x in history
            if x["difficulty"] == "Hard"
        ]

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Easy Average",
            f"{sum(easy)/len(easy):.1f}%"
            if easy else "No attempts"
        )

        col2.metric(
            "Medium Average",
            f"{sum(medium)/len(medium):.1f}%"
            if medium else "No attempts"
        )

        col3.metric(
            "Hard Average",
            f"{sum(hard)/len(hard):.1f}%"
            if hard else "No attempts"
        )

        st.subheader("Quiz History")

        for item in reversed(history):

            with st.expander(
                f"{item['date']} | {item['difficulty']} | "
                f"{item['score']}/{item['total']}"
            ):

                st.write(
                    f"Accuracy: {item['percentage']}%"
                )

                st.progress(
                    item["percentage"] / 100
                )

    else:
        st.info(
            "No quiz attempts recorded yet. "
            "Complete a DSA Quiz to see your performance."
        )

    st.divider()

    # ======================================
    # RESET
    # ======================================

    with st.expander("Reset Learning Progress"):

        st.warning(
            "This permanently deletes saved topic progress "
            "and quiz history."
        )

        confirm = st.checkbox(
            "I understand and want to reset my progress."
        )

        if st.button(
            "Reset All Progress",
            disabled=not confirm
        ):

            save_progress({
                "completed_topics": [],
                "quiz_history": []
            })

            st.success("Progress reset successfully.")
            st.rerun()
