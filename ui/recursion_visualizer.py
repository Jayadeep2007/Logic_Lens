
import streamlit as st


# =====================================
# FACTORIAL RECURSION
# =====================================

def factorial(n, steps):

    steps.append(f"factorial({n}) called")

    if n <= 1:
        steps.append(f"Base case: factorial({n}) = 1")
        return 1

    result = n * factorial(n - 1, steps)

    steps.append(f"Returning: {n} * factorial({n-1}) = {result}")

    return result


# =====================================
# FIBONACCI RECURSION
# =====================================

def fibonacci(n, steps):

    steps.append(f"fibonacci({n}) called")

    if n == 0:
        steps.append("Base case: fibonacci(0) = 0")
        return 0

    if n == 1:
        steps.append("Base case: fibonacci(1) = 1")
        return 1

    result = (
        fibonacci(n - 1, steps)
        + fibonacci(n - 2, steps)
    )

    steps.append(f"Returning: fibonacci({n}) = {result}")

    return result


# =====================================
# SUM OF N NUMBERS
# =====================================

def recursive_sum(n, steps):

    steps.append(f"sum({n}) called")

    if n == 0:
        steps.append("Base case: sum(0) = 0")
        return 0

    result = n + recursive_sum(n - 1, steps)

    steps.append(f"Returning: {n} + sum({n-1}) = {result}")

    return result


# =====================================
# MAIN VISUALIZER
# =====================================

def render_recursion_visualizer():

    st.title("🔁 Recursion Visualizer")

    st.write(
        "Understand how recursive functions work "
        "through function calls, base cases and return values."
    )

    st.divider()

    # Select algorithm
    st.subheader("1. Choose Recursion Example")

    operation = st.selectbox(
        "Select an operation",
        [
            "Factorial",
            "Fibonacci",
            "Sum of N Numbers"
        ]
    )

    # User input
    st.subheader("2. Enter Input")

    if operation == "Factorial":

        number = st.number_input(
            "Enter a number",
            min_value=0,
            max_value=20,
            value=5,
            step=1
        )

    elif operation == "Fibonacci":

        number = st.number_input(
            "Enter the position",
            min_value=0,
            max_value=10,
            value=5,
            step=1
        )

    else:

        number = st.number_input(
            "Enter N",
            min_value=0,
            max_value=100,
            value=5,
            step=1
        )

    st.caption(
        "The input limits keep the recursion trace manageable."
    )

    # Run recursion
    if st.button("Run Recursion", type="primary"):

        steps = []

        if operation == "Factorial":
            result = factorial(int(number), steps)

        elif operation == "Fibonacci":
            result = fibonacci(int(number), steps)

        else:
            result = recursive_sum(int(number), steps)

        st.session_state.recursion_result = result
        st.session_state.recursion_steps = steps
        st.session_state.recursion_operation = operation
        st.session_state.recursion_input = int(number)

    # Display result
    if "recursion_result" in st.session_state:

        st.divider()

        st.subheader("3. Final Result")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Result",
                st.session_state.recursion_result
            )

        with col2:
            st.metric(
                "Function Calls",
                len([
                    step for step in st.session_state.recursion_steps
                    if step.endswith("called")
                ])
            )

        st.divider()

        # Display execution steps
        st.subheader("4. Recursion Execution Steps")

        for index, step in enumerate(
            st.session_state.recursion_steps,
            start=1
        ):

            if "Base case" in step:
                st.success(f"Step {index}: {step}")

            elif "Returning:" in step:
                st.info(f"Step {index}: {step}")

            else:
                st.write(f"Step {index}: {step}")

        st.divider()

        # Explanation
        st.subheader("5. What Happened?")

        if st.session_state.recursion_operation == "Factorial":

            st.write(
                "The function repeatedly multiplies the current "
                "number by the factorial of the previous number "
                "until it reaches the base case."
            )

        elif st.session_state.recursion_operation == "Fibonacci":

            st.write(
                "Each Fibonacci call creates two smaller calls: "
                "fibonacci(n-1) and fibonacci(n-2). "
                "The results are added together."
            )

        else:

            st.write(
                "The function adds the current number to the "
                "sum of all previous numbers until it reaches zero."
            )

    else:

        st.info(
            "Choose an operation, enter a number and click "
            "'Run Recursion' to see the execution."
        )
