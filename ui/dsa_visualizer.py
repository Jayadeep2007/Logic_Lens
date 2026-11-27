
# pages/dsa_visualizer.py

import streamlit as st

from modules import arrays


def render_array_visualizer():

    st.title("📊 Array Visualizer")

    st.write(
        "Enter your own array values and explore "
        "how different array operations work."
    )

    st.divider()

    # --------------------------------
    # SESSION STATE INITIALIZATION
    # --------------------------------

    if "logic_array" not in st.session_state:
        st.session_state.logic_array = []

    if "array_steps" not in st.session_state:
        st.session_state.array_steps = []

    if "array_step_index" not in st.session_state:
        st.session_state.array_step_index = 0

    if "array_message" not in st.session_state:
        st.session_state.array_message = ""

    # --------------------------------
    # ARRAY INPUT
    # --------------------------------

    st.subheader("1. Create Your Array")

    with st.form("array_creation_form"):

        user_input = st.text_input(
            "Enter array elements separated by commas",
            placeholder="Example: 10, 20, 30, 40, 50"
        )

        create_button = st.form_submit_button(
            "Create Array",
            type="primary"
        )

        if create_button:

            try:
                values = [
                    int(x.strip())
                    for x in user_input.split(",")
                    if x.strip()
                ]

                if not values:
                    st.error("Please enter at least one element.")

                elif len(values) > 100:
                    st.error("Maximum 100 elements are allowed.")

                else:
                    st.session_state.logic_array = arrays.create_array(values)

                    st.session_state.array_steps = []
                    st.session_state.array_step_index = 0

                    st.success("Array created successfully!")

            except ValueError:
                st.error("Please enter valid integer values.")

    # --------------------------------
    # DISPLAY ARRAY
    # --------------------------------

    arr = st.session_state.logic_array

    st.divider()

    st.subheader("2. Current Array")

    if not arr:

        st.info("Create an array to begin.")

        return

    st.write(f"Array size: **{len(arr)}**")

    columns = st.columns(min(len(arr), 8))

    for i, value in enumerate(arr):

        with columns[i % len(columns)]:

            st.markdown(
                f"""
                <div style="
                    background-color:#172554;
                    border:1px solid #3B82F6;
                    border-radius:10px;
                    padding:15px 5px;
                    text-align:center;
                    margin-bottom:10px;
                ">
                    <div style="color:#93C5FD;font-size:12px;">
                        INDEX {i}
                    </div>
                    <div style="
                        color:white;
                        font-size:24px;
                        font-weight:bold;
                    ">
                        {value}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.code(f"Array = {arr}", language="python")

    st.divider()

    # --------------------------------
    # SELECT OPERATION
    # --------------------------------

    st.subheader("3. Perform Array Operations")

    operation = st.selectbox(
        "Choose an operation",
        [
            "Insert",
            "Delete",
            "Update",
            "Search",
            "Sort",
            "Reverse"
        ]
    )

    new_steps = []
    operation_message = ""

    # --------------------------------
    # INSERT
    # --------------------------------

    if operation == "Insert":

        col1, col2 = st.columns(2)

        with col1:
            index = st.number_input(
                "Insertion Index",
                min_value=0,
                max_value=len(arr),
                value=len(arr),
                step=1
            )

        with col2:
            value = st.number_input(
                "Value to Insert",
                value=0,
                step=1
            )

        if st.button("Execute Insert", type="primary"):

            new_array = arrays.insert_element(
                arr, int(index), int(value)
            )

            new_steps = [
                {
                    "array": arr.copy(),
                    "message": "Starting array.",
                },
                {
                    "array": new_array,
                    "message": (
                        f"Inserted {value} at index {index}."
                    ),
                }
            ]

            operation_message = "Insertion completed!"

    # --------------------------------
    # DELETE
    # --------------------------------

    elif operation == "Delete":

        index = st.number_input(
            "Index to Delete",
            min_value=0,
            max_value=len(arr) - 1,
            value=0,
            step=1
        )

        if st.button("Execute Delete", type="primary"):

            new_array = arrays.delete_element(
                arr, int(index)
            )

            new_steps = [
                {
                    "array": arr.copy(),
                    "message": "Starting array.",
                },
                {
                    "array": new_array,
                    "message": (
                        f"Deleted element at index {index}."
                    ),
                }
            ]

            operation_message = "Deletion completed!"

    # --------------------------------
    # UPDATE
    # --------------------------------

    elif operation == "Update":

        col1, col2 = st.columns(2)

        with col1:
            index = st.number_input(
                "Index to Update",
                min_value=0,
                max_value=len(arr) - 1,
                value=0,
                step=1
            )

        with col2:
            value = st.number_input(
                "New Value",
                value=0,
                step=1
            )

        if st.button("Execute Update", type="primary"):

            old_value = arr[int(index)]

            new_array = arrays.update_element(
                arr, int(index), int(value)
            )

            new_steps = [
                {
                    "array": arr.copy(),
                    "message": f"Current value is {old_value}.",
                },
                {
                    "array": new_array,
                    "message": (
                        f"Updated index {index} "
                        f"from {old_value} to {value}."
                    ),
                }
            ]

            operation_message = "Update completed!"

    # --------------------------------
    # SEARCH
    # --------------------------------

    elif operation == "Search":

        target = st.number_input(
            "Enter the value to search",
            value=0,
            step=1
        )

        if st.button("Execute Search", type="primary"):

            found_index = -1

            new_steps = []

            for i, element in enumerate(arr):

                new_steps.append({
                    "array": arr.copy(),
                    "message": (
                        f"Comparing {element} with {target} "
                        f"at index {i}."
                    ),
                })

                if element == target:
                    found_index = i
                    break

            if found_index != -1:

                operation_message = (
                    f"Found {target} at index {found_index}!"
                )

            else:

                operation_message = (
                    f"{target} was not found in the array."
                )

            new_steps.append({
                "array": arr.copy(),
                "message": operation_message
            })

    # --------------------------------
    # SORT
    # --------------------------------

    elif operation == "Sort":

        if st.button("Execute Sort", type="primary"):

            steps = arrays.bubble_sort_steps(arr)

            new_steps = [
                {
                    "array": step,
                    "message": (
                        f"Sorting step {i}: "
                        f"Comparing adjacent elements."
                    )
                }
                for i, step in enumerate(steps)
            ]

            operation_message = "Sorting completed!"

    # --------------------------------
    # REVERSE
    # --------------------------------

    elif operation == "Reverse":

        if st.button("Execute Reverse", type="primary"):

            steps = arrays.reverse_steps(arr)

            new_steps = [
                {
                    "array": step,
                    "message": (
                        f"Reversal step {i}: "
                        f"Swapping elements from both ends."
                    )
                }
                for i, step in enumerate(steps)
            ]

            operation_message = "Reversal completed!"

    # --------------------------------
    # SAVE EXECUTION HISTORY
    # --------------------------------

    if new_steps:

        st.session_state.array_steps = new_steps

        st.session_state.array_step_index = 0

        st.session_state.array_message = operation_message

        # Apply final result only for modifying operations.
        if operation in [
            "Insert",
            "Delete",
            "Update",
            "Sort",
            "Reverse"
        ]:

            st.session_state.logic_array = (
                new_steps[-1]["array"].copy()
            )

        st.rerun()

    # --------------------------------
    # STEP-BY-STEP VISUALIZATION
    # --------------------------------

    if st.session_state.array_steps:

        st.divider()

        st.subheader("4. Step-by-Step Execution")

        steps = st.session_state.array_steps

        current = st.session_state.array_step_index

        st.write(
            f"Step {current + 1} of {len(steps)}"
        )

        current_step = steps[current]

        st.info(current_step["message"])

        st.markdown("**Array State**")

        step_columns = st.columns(
            min(len(current_step["array"]), 8)
        )

        for i, value in enumerate(current_step["array"]):

            with step_columns[i % len(step_columns)]:

                st.metric(
                    label=f"Index {i}",
                    value=value
                )

        previous_col, next_col = st.columns(2)

        with previous_col:

            if st.button(
                "⬅ Previous Step",
                disabled=current == 0,
                use_container_width=True
            ):

                st.session_state.array_step_index -= 1
                st.rerun()

        with next_col:

            if st.button(
                "Next Step ➡",
                disabled=current == len(steps) - 1,
                use_container_width=True
            ):

                st.session_state.array_step_index += 1
                st.rerun()

        st.caption(
            "Use Previous Step and Next Step to explore execution."
        )

    # --------------------------------
    # COMPLEXITY INFORMATION
    # --------------------------------

    st.divider()

    st.subheader("5. Time and Space Complexity")

    complexity = {
        "Insert": ("O(n)", "O(n)"),
        "Delete": ("O(n)", "O(n)"),
        "Update": ("O(1)", "O(n)"),
        "Search": ("O(n)", "O(1)"),
        "Sort": ("O(n²)", "O(n)"),
        "Reverse": ("O(n)", "O(n)")
    }

    time, space = complexity[operation]

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Time Complexity", time)

    with col2:
        st.metric("Space Complexity", space)

    if st.session_state.array_message:

        st.success(st.session_state.array_message)
