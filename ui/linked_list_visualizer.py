
# ui/linked_list_visualizer.py

import streamlit as st

from modules.linked_lists import LinkedList


def render_linked_list_visualizer():

    st.title("🔗 Linked List Visualizer")

    st.write(
        "Create and manipulate linked lists using your own values."
    )

    st.divider()

    # --------------------------------
    # SESSION STATE
    # --------------------------------

    if "linked_values" not in st.session_state:
        st.session_state.linked_values = []

    if "linked_type" not in st.session_state:
        st.session_state.linked_type = "Singly"

    if "linked_steps" not in st.session_state:
        st.session_state.linked_steps = []

    if "linked_step_index" not in st.session_state:
        st.session_state.linked_step_index = 0

    if "linked_message" not in st.session_state:
        st.session_state.linked_message = ""

    # --------------------------------
    # SELECT LINKED LIST TYPE
    # --------------------------------

    st.subheader("1. Select Linked List Type")

    list_type = st.selectbox(
        "Choose your linked list",
        [
            "Singly",
            "Doubly",
            "Circular"
        ],
        key="linked_type_selector"
    )

    if list_type != st.session_state.linked_type:

        st.session_state.linked_type = list_type
        st.session_state.linked_values = []
        st.session_state.linked_steps = []
        st.session_state.linked_step_index = 0

    st.info(f"Selected type: {list_type} Linked List")

    # --------------------------------
    # CREATE LINKED LIST
    # --------------------------------

    st.subheader("2. Create Your Linked List")

    with st.form("linked_list_creation"):

        user_input = st.text_input(
            "Enter node values separated by commas",
            placeholder="Example: 10, 20, 30, 40"
        )

        create_button = st.form_submit_button(
            "Create Linked List",
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
                    st.error("Please enter at least one value.")

                elif len(values) > 100:
                    st.error("Maximum 100 nodes allowed.")

                else:

                    st.session_state.linked_values = values
                    st.session_state.linked_steps = []
                    st.session_state.linked_step_index = 0

                    st.success("Linked List created successfully!")

            except ValueError:

                st.error("Please enter valid integer values.")

    # --------------------------------
    # BUILD LINKED LIST
    # --------------------------------

    values = st.session_state.linked_values

    linked_list = LinkedList(list_type)
    linked_list.create(values)

    # --------------------------------
    # VISUALIZE NODES
    # --------------------------------

    st.divider()

    st.subheader("3. Linked List Visualization")

    if not values:

        st.info("Create a linked list to start.")

        return

    st.write(f"Total Nodes: **{linked_list.length()}**")

    st.markdown("**HEAD →**")

    # Display nodes in groups of six
    for start in range(0, len(values), 6):

        group = values[start:start + 6]

        columns = st.columns(min(len(group), 6))

        for j, value in enumerate(group):

            index = start + j

            with columns[j]:

                previous = (
                    values[index - 1]
                    if index > 0 and list_type == "Doubly"
                    else "NULL"
                )

                next_value = (
                    values[index + 1]
                    if index < len(values) - 1
                    else (
                        values[0]
                        if list_type == "Circular"
                        else "NULL"
                    )
                )

                st.markdown(
                    f"""
                    <div style="
                        background:#172554;
                        border:1px solid #3B82F6;
                        border-radius:12px;
                        padding:12px 5px;
                        text-align:center;
                        min-height:100px;
                    ">
                        <div style="color:#93C5FD;font-size:12px;">
                            NODE {index}
                        </div>
                        <div style="
                            color:white;
                            font-size:25px;
                            font-weight:bold;
                            margin:8px;
                        ">
                            {value}
                        </div>
                        <div style="color:#93C5FD;font-size:11px;">
                            PREV: {previous}
                        </div>
                        <div style="color:#34D399;font-size:11px;">
                            NEXT: {next_value}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            if j < len(group) - 1:
                with columns[j]:
                    st.caption("↓")

        if start + 6 < len(values):
            st.caption("Continue →")

    if list_type == "Circular":
        st.success(
            f"TAIL ({values[-1]}) points back to HEAD ({values[0]})."
        )
    else:
        st.caption(f"TAIL → {values[-1]} → NULL")

    # --------------------------------
    # POINTER DETAILS
    # --------------------------------

    with st.expander("View Node Pointer Details"):

        pointer_data = linked_list.get_pointer_info()

        for i, node in enumerate(pointer_data):

            st.write(
                f"Node {i}: DATA = {node['data']} | "
                f"PREV = {node['previous']} | "
                f"NEXT = {node['next']}"
            )

    st.divider()

    # --------------------------------
    # OPERATIONS
    # --------------------------------

    st.subheader("4. Perform Operations")

    operation = st.selectbox(
        "Select an operation",
        [
            "Insert at Beginning",
            "Insert at End",
            "Insert at Position",
            "Delete by Value",
            "Delete by Position",
            "Search",
            "Reverse"
        ]
    )

    new_steps = []
    message = ""

    # --------------------------------
    # INSERT BEGINNING
    # --------------------------------

    if operation == "Insert at Beginning":

        value = st.number_input(
            "Enter new node value",
            value=0,
            step=1
        )

        if st.button("Execute Operation", type="primary"):

            old = values.copy()

            linked_list.insert_beginning(int(value))

            new_steps = [
                {"values": old, "message": "Original linked list."},
                {
                    "values": linked_list.to_list(),
                    "message": f"Inserted {value} at the beginning."
                }
            ]

            message = "Node inserted at beginning!"

    # --------------------------------
    # INSERT END
    # --------------------------------

    elif operation == "Insert at End":

        value = st.number_input(
            "Enter new node value",
            value=0,
            step=1
        )

        if st.button("Execute Operation", type="primary"):

            old = values.copy()

            linked_list.insert_end(int(value))

            new_steps = [
                {"values": old, "message": "Original linked list."},
                {
                    "values": linked_list.to_list(),
                    "message": f"Inserted {value} at the end."
                }
            ]

            message = "Node inserted at end!"

    # --------------------------------
    # INSERT POSITION
    # --------------------------------

    elif operation == "Insert at Position":

        col1, col2 = st.columns(2)

        with col1:

            position = st.number_input(
                "Position",
                min_value=0,
                max_value=len(values),
                value=0,
                step=1
            )

        with col2:

            value = st.number_input(
                "Node Value",
                value=0,
                step=1
            )

        if st.button("Execute Operation", type="primary"):

            old = values.copy()

            linked_list.insert_position(
                int(position),
                int(value)
            )

            new_steps = [
                {"values": old, "message": "Original linked list."},
                {
                    "values": linked_list.to_list(),
                    "message": (
                        f"Inserted {value} at position {position}."
                    )
                }
            ]

            message = "Insertion completed!"

    # --------------------------------
    # DELETE BY VALUE
    # --------------------------------

    elif operation == "Delete by Value":

        value = st.number_input(
            "Enter value to delete",
            value=0,
            step=1
        )

        if st.button("Execute Operation", type="primary"):

            old = values.copy()

            deleted = linked_list.delete_value(int(value))

            if deleted:

                new_steps = [
                    {"values": old, "message": "Original linked list."},
                    {
                        "values": linked_list.to_list(),
                        "message": f"Deleted first occurrence of {value}."
                    }
                ]

                message = f"Value {value} deleted successfully!"

            else:

                message = f"Value {value} was not found."

                new_steps = [
                    {
                        "values": old,
                        "message": message
                    }
                ]

    # --------------------------------
    # DELETE BY POSITION
    # --------------------------------

    elif operation == "Delete by Position":

        position = st.number_input(
            "Enter position to delete",
            min_value=0,
            max_value=len(values) - 1,
            value=0,
            step=1
        )

        if st.button("Execute Operation", type="primary"):

            old = values.copy()

            deleted = linked_list.delete_position(int(position))

            new_steps = [
                {"values": old, "message": "Original linked list."},
                {
                    "values": linked_list.to_list(),
                    "message": (
                        f"Deleted node with value {deleted} "
                        f"at position {position}."
                    )
                }
            ]

            message = f"Deleted node containing {deleted}!"

    # --------------------------------
    # SEARCH
    # --------------------------------

    elif operation == "Search":

        target = st.number_input(
            "Enter value to search",
            value=0,
            step=1
        )

        if st.button("Execute Operation", type="primary"):

            found_index, search_steps = linked_list.search(
                int(target)
            )

            new_steps = search_steps

            if found_index != -1:

                message = (
                    f"Value {target} found at position {found_index}."
                )

                new_steps.append({
                    "values": values.copy(),
                    "highlight": found_index,
                    "message": message
                })

            else:

                message = f"Value {target} not found."

                new_steps.append({
                    "values": values.copy(),
                    "highlight": -1,
                    "message": message
                })

    # --------------------------------
    # REVERSE
    # --------------------------------

    elif operation == "Reverse":

        if st.button("Execute Operation", type="primary"):

            old = values.copy()

            linked_list.reverse()

            new_steps = [
                {"values": old, "message": "Original linked list."},
                {
                    "values": linked_list.to_list(),
                    "message": (
                        "Reversed the node order and rebuilt pointers."
                    )
                }
            ]

            message = "Linked list reversed successfully!"

    # --------------------------------
    # SAVE RESULTS
    # --------------------------------

    if new_steps:

        st.session_state.linked_steps = new_steps
        st.session_state.linked_step_index = 0
        st.session_state.linked_message = message

        # Update actual list only for modifying operations
        if operation != "Search":

            st.session_state.linked_values = (
                new_steps[-1]["values"].copy()
            )

        st.rerun()

    # --------------------------------
    # STEP BY STEP EXECUTION
    # --------------------------------

    if st.session_state.linked_steps:

        st.divider()

        st.subheader("5. Step-by-Step Execution")

        steps = st.session_state.linked_steps

        current = st.session_state.linked_step_index

        current_step = steps[current]

        st.write(
            f"Step {current + 1} of {len(steps)}"
        )

        st.info(current_step["message"])

        step_values = current_step["values"]

        if step_values:

            highlight = current_step.get("highlight", -1)

            step_columns = st.columns(
                min(len(step_values), 6)
            )

            for i, value in enumerate(step_values):

                with step_columns[i % len(step_columns)]:

                    if i == highlight:

                        st.success(
                            f"NODE {i}\n\n**{value}**"
                        )

                    else:

                        st.metric(
                            f"NODE {i}",
                            value
                        )

        else:

            st.info("The linked list is empty.")

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "⬅ Previous Step",
                disabled=current == 0,
                use_container_width=True
            ):

                st.session_state.linked_step_index -= 1
                st.rerun()

        with col2:

            if st.button(
                "Next Step ➡",
                disabled=current == len(steps) - 1,
                use_container_width=True
            ):

                st.session_state.linked_step_index += 1
                st.rerun()

        if st.session_state.linked_message:

            st.success(st.session_state.linked_message)

    # --------------------------------
    # COMPLEXITY INFORMATION
    # --------------------------------

    st.divider()

    st.subheader("6. Complexity Analysis")

    complexity = {
        "Insert at Beginning": ("O(1)", "O(1)"),
        "Insert at End": ("O(1)", "O(1)"),
        "Insert at Position": ("O(n)", "O(1)"),
        "Delete by Value": ("O(n)", "O(1)"),
        "Delete by Position": ("O(n)", "O(1)"),
        "Search": ("O(n)", "O(1)"),
        "Reverse": ("O(n)", "O(1)")
    }

    time, space = complexity[operation]

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Time Complexity", time)

    with col2:
        st.metric("Auxiliary Space", space)
