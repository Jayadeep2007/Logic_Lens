
import streamlit as st

from ui.progress_dashboard import record_quiz_result
# ==================================================
# QUESTION BANK
# ==================================================

QUESTIONS = {
    "Easy": [
        {
            "question": "Which data structure follows LIFO?",
            "options": [
                "Queue",
                "Stack",
                "Array",
                "Linked List"
            ],
            "answer": "Stack",
            "explanation": "Stack follows Last In, First Out (LIFO)."
        },
        {
            "question": "Which data structure follows FIFO?",
            "options": [
                "Stack",
                "Tree",
                "Queue",
                "Graph"
            ],
            "answer": "Queue",
            "explanation": "Queue follows First In, First Out (FIFO)."
        },
        {
            "question": "What is the first index of a Python list?",
            "options": [
                "0",
                "1",
                "-1",
                "2"
            ],
            "answer": "0",
            "explanation": "Python list indexing starts from index 0."
        },
        {
            "question": "Which algorithm checks elements one by one?",
            "options": [
                "Binary Search",
                "Linear Search",
                "Merge Sort",
                "Quick Sort"
            ],
            "answer": "Linear Search",
            "explanation": "Linear Search checks each element sequentially."
        },
        {
            "question": "Which traversal visits the root first?",
            "options": [
                "Inorder",
                "Postorder",
                "Preorder",
                "Level Order"
            ],
            "answer": "Preorder",
            "explanation": "Preorder traversal follows Root, Left, Right."
        }
    ],

    "Medium": [
        {
            "question": "What is the average time complexity of Binary Search?",
            "options": [
                "O(n)",
                "O(log n)",
                "O(n²)",
                "O(1)"
            ],
            "answer": "O(log n)",
            "explanation": "Binary Search halves the search interval in every iteration."
        },
        {
            "question": "Which sorting algorithm uses divide and conquer?",
            "options": [
                "Bubble Sort",
                "Selection Sort",
                "Merge Sort",
                "Insertion Sort"
            ],
            "answer": "Merge Sort",
            "explanation": "Merge Sort divides the array, sorts each half and merges them."
        },
        {
            "question": "Which data structure is commonly used in BFS?",
            "options": [
                "Stack",
                "Queue",
                "Heap",
                "Array only"
            ],
            "answer": "Queue",
            "explanation": "BFS uses a queue to process nodes level by level."
        },
        {
            "question": "What is the worst-case time complexity of Quick Sort?",
            "options": [
                "O(n)",
                "O(log n)",
                "O(n log n)",
                "O(n²)"
            ],
            "answer": "O(n²)",
            "explanation": "Poor pivot choices can create highly unbalanced partitions."
        },
        {
            "question": "Which technique stores results of overlapping subproblems?",
            "options": [
                "Greedy Method",
                "Dynamic Programming",
                "Linear Search",
                "DFS"
            ],
            "answer": "Dynamic Programming",
            "explanation": "Dynamic Programming stores previously computed results for reuse."
        }
    ],

    "Hard": [
        {
            "question": "What is the time complexity of Dijkstra's algorithm using an adjacency list and a binary heap?",
            "options": [
                "O(V + E)",
                "O((V + E) log V)",
                "O(V²)",
                "O(E²)"
            ],
            "answer": "O((V + E) log V)",
            "explanation": "With a binary heap and adjacency list, the usual complexity is O((V + E) log V)."
        },
        {
            "question": "Which algorithm finds a Minimum Spanning Tree using a greedy strategy?",
            "options": [
                "KMP",
                "Prim's Algorithm",
                "Binary Search",
                "Floyd-Warshall"
            ],
            "answer": "Prim's Algorithm",
            "explanation": "Prim's algorithm repeatedly adds the minimum-weight edge connecting the current tree to a new vertex."
        },
        {
            "question": "What is the time complexity of building a heap from an array?",
            "options": [
                "O(n)",
                "O(n log n)",
                "O(log n)",
                "O(n²)"
            ],
            "answer": "O(n)",
            "explanation": "Bottom-up heap construction takes linear time."
        },
        {
            "question": "Which algorithm is commonly used to find the Longest Common Subsequence?",
            "options": [
                "DFS",
                "Dynamic Programming",
                "Prim's Algorithm",
                "Linear Search"
            ],
            "answer": "Dynamic Programming",
            "explanation": "LCS uses a DP table to solve smaller prefix problems."
        },
        {
            "question": "What is the maximum number of edges in a simple undirected graph with V vertices?",
            "options": [
                "V",
                "V²",
                "V(V - 1) / 2",
                "V - 1"
            ],
            "answer": "V(V - 1) / 2",
            "explanation": "Every pair of distinct vertices can have at most one edge."
        }
    ]
}


# ==================================================
# INITIALIZE QUIZ STATE
# ==================================================

def initialize_quiz():

    defaults = {
        "quiz_active": False,
        "quiz_difficulty": "Easy",
        "quiz_index": 0,
        "quiz_score": 0,
        "quiz_submitted": False,
        "quiz_answers": [],
        "quiz_questions": []
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ==================================================
# START QUIZ
# ==================================================

def start_quiz(difficulty):

    st.session_state["quiz_difficulty"] = difficulty
    st.session_state["quiz_questions"] = QUESTIONS[difficulty].copy()
    st.session_state["quiz_index"] = 0
    st.session_state["quiz_score"] = 0
    st.session_state["quiz_submitted"] = False
    st.session_state["quiz_answers"] = []
    st.session_state["quiz_active"] = True


# ==================================================
# SUBMIT ANSWER
# ==================================================

def submit_answer():

    if st.session_state["quiz_submitted"]:
        return

    index = st.session_state["quiz_index"]
    questions = st.session_state["quiz_questions"]

    selected = st.session_state.get(
        f"quiz_option_{index}"
    )

    if selected is None:
        return

    question = questions[index]

    correct = selected == question["answer"]

    if correct:
        st.session_state["quiz_score"] += 1

    st.session_state["quiz_answers"].append({
        "selected": selected,
        "correct": correct
    })

    st.session_state["quiz_submitted"] = True


# ==================================================
# NEXT QUESTION
# ==================================================

def next_question():

    st.session_state["quiz_index"] += 1
    st.session_state["quiz_submitted"] = False


# ==================================================
# MAIN QUIZ VISUALIZER
# ==================================================

def render_quiz_visualizer():

    initialize_quiz()

    st.title("🎯 LogicLens DSA Quiz")

    st.write(
        "Test your Data Structures and Algorithms knowledge "
        "with interactive multiple-choice questions."
    )

    st.divider()

    # ----------------------------------------------
    # QUIZ START SCREEN
    # ----------------------------------------------

    if not st.session_state["quiz_active"]:

        st.subheader("Choose Your Difficulty")

        difficulty = st.selectbox(
            "Select Level",
            ["Easy", "Medium", "Hard"],
            key="quiz_level_selection"
        )

        difficulty_info = {
            "Easy": "Beginner-friendly DSA questions.",
            "Medium": "Questions about algorithms and complexity.",
            "Hard": "Advanced algorithm and graph questions."
        }

        st.info(difficulty_info[difficulty])

        st.markdown("""
        ### Quiz Instructions

        - Each quiz contains 5 questions.
        - Every correct answer earns 1 point.
        - Incorrect answers earn 0 points.
        - You will see an explanation after each answer.
        - Your final score appears at the end.
        """)

        st.button(
            "🚀 Start Quiz",
            type="primary",
            use_container_width=True,
            on_click=start_quiz,
            args=(difficulty,)
        )

        return

    # ----------------------------------------------
    # QUIZ QUESTIONS
    # ----------------------------------------------

    questions = st.session_state["quiz_questions"]
    index = st.session_state["quiz_index"]

    total = len(questions)

    # ----------------------------------------------
    # FINAL RESULT
    # ----------------------------------------------

    if index >= total:

        score = st.session_state["quiz_score"]
        if not st.session_state.get("quiz_result_saved", False):
            record_quiz_result(
                st.session_state["quiz_difficulty"],
                score,
                total
    )

            st.session_state["quiz_result_saved"] = True

        percentage = (score / total) * 100

        st.balloons()

        st.subheader("🏆 Quiz Completed!")

        st.metric(
            "Your Final Score",
            f"{score} / {total}"
        )

        st.progress(percentage / 100)

        st.write(f"Your accuracy: {percentage:.0f}%")

        if percentage == 100:
            st.success("Excellent! Perfect score!")

        elif percentage >= 60:
            st.success("Good work! Keep practising.")

        else:
            st.warning("Keep learning. You can improve your score!")

        st.subheader("Answer Summary")

        for i, (question, answer) in enumerate(
            zip(questions, st.session_state["quiz_answers"])
        ):

            st.write(f"**Question {i + 1}:** {question['question']}")

            st.write(
                f"Your answer: {answer['selected']}"
            )

            if answer["correct"]:
                st.success("Correct")
            else:
                st.error(
                    f"Correct answer: {question['answer']}"
                )

        st.button(
            "🔄 Restart Quiz",
            type="primary",
            use_container_width=True,
            on_click=start_quiz,
            args=(st.session_state["quiz_difficulty"],)
        )

        return

    # ----------------------------------------------
    # QUESTION DISPLAY
    # ----------------------------------------------

    question = questions[index]

    st.markdown(
        f"### Question {index + 1} of {total}"
    )

    st.progress((index + 1) / total)

    st.caption(
        f"Difficulty: {st.session_state['quiz_difficulty']}"
    )

    st.markdown(f"### {question['question']}")

    option_key = f"quiz_option_{index}"

    st.radio(
        "Choose your answer:",
        question["options"],
        index=None,
        key=option_key,
        disabled=st.session_state["quiz_submitted"]
    )

    # ----------------------------------------------
    # SUBMIT ANSWER
    # ----------------------------------------------

    if not st.session_state["quiz_submitted"]:

        selected = st.session_state.get(option_key)

        st.button(
            "Submit Answer",
            type="primary",
            disabled=selected is None,
            use_container_width=True,
            on_click=submit_answer
        )

    # ----------------------------------------------
    # SHOW FEEDBACK
    # ----------------------------------------------

    if st.session_state["quiz_submitted"]:

        answer = st.session_state["quiz_answers"][-1]

        if answer["correct"]:
            st.success("🎉 Correct Answer!")

        else:
            st.error(
                f"Incorrect! The correct answer is "
                f"{question['answer']}."
            )

        st.info(
            f"Explanation: {question['explanation']}"
        )

        st.write(
            f"Current Score: {st.session_state['quiz_score']} / {total}"
        )

        if index + 1 < total:

            st.button(
                "Next Question →",
                type="primary",
                use_container_width=True,
                on_click=next_question
            )

        else:

            st.button(
                "View Final Result →",
                type="primary",
                use_container_width=True,
                on_click=next_question
            )
