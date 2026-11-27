
import streamlit as st
import subprocess
import sys
import tempfile
import os


def run_python_code(code):
    """Run Python code locally and capture its output."""

    file_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False,
            encoding="utf-8"
        ) as file:
            file.write(code)
            file_path = file.name

        result = subprocess.run(
            [sys.executable, "-I", file_path],
            capture_output=True,
            text=True,
            timeout=5
        )

        return result.stdout, result.stderr, result.returncode

    except subprocess.TimeoutExpired:
        return "", "Execution timed out (5 seconds).", 1

    except Exception as error:
        return "", str(error), 1

    finally:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)


def render_code_playground():

    st.title("💻 LogicLens Code Playground")

    st.write(
        "Write, execute and experiment with Python programs."
    )

    st.markdown("---")

    # Sample programs
    samples = {
        "Hello World": "print('Welcome to LogicLens!')",

        "Array Example": """
numbers = [10, 20, 30, 40, 50]

print("Array:", numbers)
print("First element:", numbers[0])
print("Array length:", len(numbers))
""",

        "Stack Example": """
stack = []

stack.append(10)
stack.append(20)
stack.append(30)

print("Stack:", stack)

removed = stack.pop()

print("Removed element:", removed)
print("Updated Stack:", stack)
""",

        "Queue Example": """
from collections import deque

queue = deque()

queue.append(10)
queue.append(20)
queue.append(30)

print("Queue:", list(queue))

removed = queue.popleft()

print("Removed element:", removed)
print("Updated Queue:", list(queue))
""",

        "Bubble Sort": """
numbers = [50, 20, 40, 10, 30]

for i in range(len(numbers)):
    for j in range(len(numbers) - i - 1):
        if numbers[j] > numbers[j + 1]:
            numbers[j], numbers[j + 1] = (
                numbers[j + 1],
                numbers[j]
            )

print("Sorted Array:", numbers)
""",

        "Binary Search": """
numbers = [10, 20, 30, 40, 50]
target = 40

low = 0
high = len(numbers) - 1
found = False

while low <= high:
    mid = (low + high) // 2

    if numbers[mid] == target:
        print("Element found at index:", mid)
        found = True
        break

    elif numbers[mid] < target:
        low = mid + 1

    else:
        high = mid - 1

if not found:
    print("Element not found")
"""
    }

    # Sample selection
    sample_name = st.selectbox(
        "Choose a Sample Program",
        list(samples.keys())
    )

    if st.button("Load Sample Program"):
        st.session_state["playground_code"] = samples[sample_name]

    # Code editor
    if "playground_code" not in st.session_state:
        st.session_state["playground_code"] = (
            "print('Hello, LogicLens!')"
        )

    st.subheader("Python Code Editor")

    code = st.text_area(
        "Write your Python code below",
        key="playground_code",
        height=350,
        label_visibility="collapsed"
    )

    # Controls
    col1, col2 = st.columns(2)

    with col1:
        run_clicked = st.button(
            "▶ Run Code",
            type="primary",
            use_container_width=True
        )

    with col2:
        clear_clicked = st.button(
            "Clear Code",
            use_container_width=True
        )

    if clear_clicked:
        st.session_state["playground_code"] = ""
        st.session_state.pop("playground_output", None)
        st.rerun()

    if run_clicked:

        if not code.strip():
            st.warning("Please write some Python code first.")

        else:
            with st.spinner("Running your program..."):

                stdout, stderr, return_code = run_python_code(code)

                st.session_state["playground_output"] = {
                    "stdout": stdout,
                    "stderr": stderr,
                    "return_code": return_code
                }

    # Output console
    st.divider()
    st.subheader("🖥️ Output Console")

    output = st.session_state.get("playground_output")

    if output is None:
        st.info("Your program output will appear here.")

    elif output["return_code"] == 0:

        st.success("Program executed successfully!")

        if output["stdout"]:
            st.code(output["stdout"], language="text")
        else:
            st.info("Program completed without printed output.")

        if output["stderr"]:
            st.warning(output["stderr"])

    else:
        st.error("Program execution failed.")

        if output["stderr"]:
            st.code(output["stderr"], language="text")

        if output["stdout"]:
            st.text("Output before error:")
            st.code(output["stdout"], language="text")

    st.caption(
        "LogicLens Python Playground | Execution limit: 5 seconds"
    )

