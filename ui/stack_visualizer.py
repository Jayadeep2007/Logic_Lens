
# ui/stack_visualizer.py

import streamlit as st
from modules.stacks import Stack


def render_stack_visualizer():

    st.title("📚 Stack Visualizer")

    st.write(
        "Explore the Last In, First Out (LIFO) "
        "principle using interactive stack operations."
    )

    st.divider()

    # SESSION STATE
    if "stack_items" not in st.session_state:
        st.session_state.stack_items = []

    if "stack_capacity" not in st.session_state:
        st.session_state.stack_capacity = 5

    if "stack_steps" not in st.session_state:
        st.session_state.stack_steps = []

    if "stack_step_index" not in st.session_state:
        st.session_state.stack_step_index = 0

    if "stack_message" not in st.session_state:
        st.session_state.stack_message = ""

    # CAPACITY
    st.subheader("1. Stack Configuration")

    capacity = st.number_input(
        "Maximum Stack Capacity",
        min_value=1,
        max_value=30,
        value=st.session_state.stack_capacity,
        step=1
    )

    if capacity != st.session_state.stack_capacity:

        st.session_state.stack_capacity = int(capacity)
        st.session_state.stack_steps = []
        st.session_state.stack_step_index = 0

        if len(st.session_state.stack_items) > capacity:
            st.session_state.stack_items = (
                st.session_state.stack_items[-int(capacity):]
            )

    # BUILD STACK
    stack = Stack(st.session_state.stack_capacity)
    stack.items = st.session_state.stack_items.copy()

    # INITIALIZE
    st.divider()
    st.subheader("2. Stack Visualization")

    items = st.session_state.stack_items

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Stack Size", len(items))

    with col2:
        st.metric("Capacity", st.session_state.stack_capacity)

    with col3:
        st.metric("Remaining Space", stack.capacity - stack.size())

    # VISUAL STACK
    st.markdown("### Current Stack")

    if not items:

        st.info("Stack is empty. Push an element to begin.")

    else:

        st.markdown(
            "<div style='text-align:center;color:#FBBF24;"
            "font-weight:bold;'>TOP ↓</div>",
            unsafe_allow_html=True
        )

        for index in range(len(items) - 1, -1, -1):

            value = items[index]

            st.markdown(
                f"""
                <div style="
                    background:#1D4ED8;
                    border:2px solid #60A5FA;
                    border-radius:8px;
                    padding:12px;
                    margin:5px auto;
                    width:65%;
                    text-align:center;
                    color:white;
                    font-size:20px;
                    font-weight:bold;
                ">
                    {value}
                    {"  ← TOP" if index == len(items)-1 else ""}
                </div>
                """,
                unsafe_allow_html=True
            )

        st.caption("BOTTOM ↑")

    st.divider()

    # OPERATIONS
    st.subheader("3. Stack Operations")

    operation = st.selectbox(
        "Choose Operation",
        [
            "Push",
            "Pop",
            "Peek",
            "Is Empty",
            "Is Full",
            "Clear Stack"
        ]
    )

    if operation == "Push":

        value = st.number_input(
            "Enter value to push",
            value=0,
            step=1
        )

        if st.button("Execute Push", type="primary"):

            try:

                old = stack.get_stack()

                stack.push(int(value))

                new = stack.get_stack()

                st.session_state.stack_items = new

                st.session_state.stack_steps = [
                    {
                        "items": old,
                        "message": "Original stack."
                    },
                    {
                        "items": new,
                        "message": f"Pushed {value} onto the stack."
                    }
                ]

                st.session_state.stack_step_index = 0

                st.session_state.stack_message = (
                    f"Successfully pushed {value}!"
                )

            except OverflowError as error:

                st.session_state.stack_message = str(error)
                st.session_state.stack_steps = []

    elif operation == "Pop":

        if st.button("Execute Pop", type="primary"):

            try:

                old = stack.get_stack()

                removed, new = stack.pop()

                st.session_state.stack_items = new

                st.session_state.stack_steps = [
                    {
                        "items": old,
                        "message": f"Top element is {removed}."
                    },
                    {
                        "items": new,
                        "message": f"Removed {removed} from the stack."
                    }
                ]

                st.session_state.stack_step_index = 0

                st.session_state.stack_message = (
                    f"Successfully popped {removed}!"
                )

            except IndexError as error:

                st.session_state.stack_message = str(error)
                st.session_state.stack_steps = []

    elif operation == "Peek":

        if st.button("Execute Peek", type="primary"):

            try:

                top = stack.peek()

                st.session_state.stack_steps = [
                    {
                        "items": stack.get_stack(),
                        "message": f"TOP element is {top}."
                    }
                ]

                st.session_state.stack_step_index = 0

                st.session_state.stack_message = (
                    f"Top element: {top}"
                )

            except IndexError as error:

                st.session_state.stack_message = str(error)

    elif operation == "Is Empty":

        if st.button("Check Stack", type="primary"):

            result = stack.is_empty()

            st.session_state.stack_message = (
                "Yes, the stack is empty."
                if result else
                "No, the stack is not empty."
            )

    elif operation == "Is Full":

        if st.button("Check Stack", type="primary"):

            result = stack.is_full()

            st.session_state.stack_message = (
                "Yes, the stack is full."
                if result else
                "No, the stack is not full."
            )

    elif operation == "Clear Stack":

        if st.button("Clear Stack", type="primary"):

            old = stack.get_stack()

            stack.clear()

            new = stack.get_stack()

            st.session_state.stack_items = new

            st.session_state.stack_steps = [
                {
                    "items": old,
                    "message": "Original stack."
                },
                {
                    "items": new,
                    "message": "All elements removed."
                }
            ]

            st.session_state.stack_step_index = 0

            st.session_state.stack_message = (
                "Stack cleared successfully!"
            )

    # SHOW MESSAGE
    if st.session_state.stack_message:

        st.info(st.session_state.stack_message)

    # STEP EXECUTION
    if st.session_state.stack_steps:

        st.divider()

        st.subheader("4. Step-by-Step Execution")

        steps = st.session_state.stack_steps

        current = st.session_state.stack_step_index

        step = steps[current]

        st.write(f"Step {current + 1} of {len(steps)}")

        st.info(step["message"])

        st.write("Stack State:")

        if step["items"]:

            for index in range(len(step["items"]) - 1, -1, -1):

                value = step["items"][index]

                st.markdown(
                    f"""
                    <div style="
                        background:#172554;
                        border:1px solid #60A5FA;
                        padding:10px;
                        border-radius:7px;
                        margin:4px auto;
                        width:55%;
                        text-align:center;
                        color:white;
                    ">
                        {value}
                        {" ← TOP" if index == len(step["items"])-1 else ""}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:

            st.warning("Stack is empty.")

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "⬅ Previous Step",
                disabled=current == 0,
                use_container_width=True
            ):

                st.session_state.stack_step_index -= 1
                st.rerun()

        with col2:

            if st.button(
                "Next Step ➡",
                disabled=current == len(steps)-1,
                use_container_width=True
            ):

                st.session_state.stack_step_index += 1
                st.rerun()

    # COMPLEXITY
    st.divider()

    st.subheader("5. Complexity Analysis")

    complexities = {
        "Push": ("O(1)", "O(1)"),
        "Pop": ("O(1)", "O(1)"),
        "Peek": ("O(1)", "O(1)"),
        "Is Empty": ("O(1)", "O(1)"),
        "Is Full": ("O(1)", "O(1)"),
        "Clear Stack": ("O(n)", "O(1)")
    }

    time, space = complexities[operation]

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Time Complexity", time)

    with col2:
        st.metric("Auxiliary Space", space)
