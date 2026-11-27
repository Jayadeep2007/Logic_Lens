
# ==========================================
# LOGICLENS - QUEUE VISUALIZER
# ==========================================

import streamlit as st
from modules.queues import Queue


def render_queue_visualizer():

    st.title("🚶 Queue Visualizer")

    st.write(
        "Explore Simple Queue, Circular Queue, "
        "Priority Queue and Deque using interactive operations."
    )

    st.divider()

    # ==========================================
    # 1. SESSION STATE
    # ==========================================

    defaults = {
        "queue_items": [],
        "queue_capacity": 5,
        "queue_type": "Simple",
        "queue_steps": [],
        "queue_step_index": 0,
        "queue_message": ""
    }

    for key, value in defaults.items():

        if key not in st.session_state:
            st.session_state[key] = value

    # ==========================================
    # 2. QUEUE CONFIGURATION
    # ==========================================

    st.subheader("1. Queue Configuration")

    queue_type = st.selectbox(
        "Select Queue Type",
        ["Simple", "Circular", "Priority", "Deque"],
        key="queue_type_selector"
    )

    if queue_type != st.session_state.queue_type:

        st.session_state.queue_type = queue_type
        st.session_state.queue_items = []
        st.session_state.queue_steps = []
        st.session_state.queue_step_index = 0
        st.session_state.queue_message = ""

    capacity = st.number_input(
        "Maximum Queue Capacity",
        min_value=1,
        max_value=30,
        value=st.session_state.queue_capacity,
        step=1
    )

    if capacity != st.session_state.queue_capacity:

        st.session_state.queue_capacity = int(capacity)

        if len(st.session_state.queue_items) > capacity:
            st.session_state.queue_items = (
                st.session_state.queue_items[:int(capacity)]
            )

        st.session_state.queue_steps = []
        st.session_state.queue_step_index = 0

    # ==========================================
    # 3. BUILD QUEUE
    # ==========================================

    queue = Queue(
        capacity=int(st.session_state.queue_capacity),
        queue_type=queue_type
    )

    queue.items = st.session_state.queue_items.copy()

    items = st.session_state.queue_items

    # ==========================================
    # 4. QUEUE STATUS
    # ==========================================

    st.divider()

    st.subheader("2. Queue Status")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Queue Size", len(items))

    with col2:
        st.metric("Capacity", queue.capacity)

    with col3:
        st.metric(
            "Available Space",
            queue.capacity - len(items)
        )

    # ==========================================
    # 5. QUEUE VISUALIZATION
    # ==========================================

    st.divider()

    st.subheader("3. Queue Visualization")

    if not items:

        st.info(
            "Queue is empty. Enqueue an element to begin."
        )

    else:

        st.markdown("### FRONT → REAR")

        max_columns = 6

        for start in range(0, len(items), max_columns):

            group = items[start:start + max_columns]

            columns = st.columns(len(group))

            for j, item in enumerate(group):

                index = start + j

                with columns[j]:

                    # Priority Queue
                    if queue_type == "Priority":

                        value = item["value"]
                        priority = item["priority"]

                        with st.container(border=True):

                            st.caption(f"INDEX {index}")

                            st.subheader(str(value))

                            st.caption(
                                f"Priority: {priority}"
                            )

                    # Other Queue Types
                    else:

                        with st.container(border=True):

                            st.caption(f"INDEX {index}")

                            st.subheader(str(item))

                    # FRONT POINTER
                    if index == 0:

                        st.success("⬇ FRONT")

                    # REAR POINTER
                    if index == len(items) - 1:

                        st.warning("⬇ REAR")

        st.divider()

        st.markdown("### Queue Pointer Information")

        col1, col2 = st.columns(2)

        if queue_type == "Priority":

            front_value = items[0]["value"]
            rear_value = items[-1]["value"]

        else:

            front_value = items[0]
            rear_value = items[-1]

        with col1:

            st.metric(
                "FRONT Element",
                str(front_value)
            )

        with col2:

            st.metric(
                "REAR Element",
                str(rear_value)
            )

        st.caption(
            f"Total Elements: {len(items)}"
        )

        if queue_type == "Circular":

            st.info(
                "Circular Queue: The rear connects back "
                "to the front conceptually."
            )

    # ==========================================
    # 6. SELECT OPERATIONS
    # ==========================================

    st.divider()

    st.subheader("4. Perform Queue Operations")

    if queue_type in ["Simple", "Circular", "Priority"]:

        operations = [
            "Enqueue",
            "Dequeue",
            "Peek",
            "Is Empty",
            "Is Full",
            "Clear Queue"
        ]

    else:

        operations = [
            "Insert Front",
            "Insert Rear",
            "Delete Front",
            "Delete Rear",
            "Peek",
            "Is Empty",
            "Is Full",
            "Clear Queue"
        ]

    operation = st.selectbox(
        "Choose an operation",
        operations,
        key="queue_operation_selector"
    )

    new_steps = []
    message = ""
    modified = False

    # ==========================================
    # 7. ENQUEUE
    # ==========================================

    if operation == "Enqueue":

        value = st.number_input(
            "Enter Element",
            value=0,
            step=1,
            key="enqueue_value"
        )

        priority = 1

        if queue_type == "Priority":

            priority = st.number_input(
                "Enter Priority",
                min_value=1,
                max_value=100,
                value=1,
                step=1,
                key="enqueue_priority"
            )

        if st.button(
            "Execute Enqueue",
            type="primary"
        ):

            old = queue.get_queue()

            try:

                queue.enqueue(
                    int(value),
                    int(priority)
                )

                updated = queue.get_queue()

                new_steps = [
                    {
                        "items": old,
                        "message": "Original queue."
                    },
                    {
                        "items": updated,
                        "message": f"Inserted {value} into the queue."
                    }
                ]

                message = f"Successfully enqueued {value}!"

                modified = True

            except OverflowError as error:

                message = str(error)

    # ==========================================
    # 8. DEQUEUE
    # ==========================================

    elif operation == "Dequeue":

        if st.button(
            "Execute Dequeue",
            type="primary"
        ):

            old = queue.get_queue()

            try:

                removed, updated = queue.dequeue()

                new_steps = [
                    {
                        "items": old,
                        "message": "Original queue."
                    },
                    {
                        "items": updated,
                        "message": f"Removed {removed} from FRONT."
                    }
                ]

                message = f"Successfully dequeued {removed}!"

                modified = True

            except IndexError as error:

                message = str(error)

    # ==========================================
    # 9. PEEK
    # ==========================================

    elif operation == "Peek":

        if st.button(
            "Execute Peek",
            type="primary"
        ):

            try:

                front = queue.peek()

                if queue_type == "Priority":

                    message = (
                        f"Front element: {front['value']}, "
                        f"Priority: {front['priority']}."
                    )

                else:

                    message = f"Front element is {front}."

                new_steps = [
                    {
                        "items": queue.get_queue(),
                        "message": message
                    }
                ]

            except IndexError as error:

                message = str(error)

    # ==========================================
    # 10. INSERT FRONT
    # ==========================================

    elif operation == "Insert Front":

        value = st.number_input(
            "Enter Element",
            value=0,
            step=1,
            key="insert_front_value"
        )

        if st.button(
            "Execute Insert Front",
            type="primary"
        ):

            old = queue.get_queue()

            try:

                queue.insert_front(int(value))

                updated = queue.get_queue()

                new_steps = [
                    {
                        "items": old,
                        "message": "Original deque."
                    },
                    {
                        "items": updated,
                        "message": f"Inserted {value} at FRONT."
                    }
                ]

                message = "Front insertion successful!"

                modified = True

            except OverflowError as error:

                message = str(error)

    # ==========================================
    # 11. INSERT REAR
    # ==========================================

    elif operation == "Insert Rear":

        value = st.number_input(
            "Enter Element",
            value=0,
            step=1,
            key="insert_rear_value"
        )

        if st.button(
            "Execute Insert Rear",
            type="primary"
        ):

            old = queue.get_queue()

            try:

                queue.insert_rear(int(value))

                updated = queue.get_queue()

                new_steps = [
                    {
                        "items": old,
                        "message": "Original deque."
                    },
                    {
                        "items": updated,
                        "message": f"Inserted {value} at REAR."
                    }
                ]

                message = "Rear insertion successful!"

                modified = True

            except OverflowError as error:

                message = str(error)

    # ==========================================
    # 12. DELETE FRONT
    # ==========================================

    elif operation == "Delete Front":

        if st.button(
            "Execute Delete Front",
            type="primary"
        ):

            old = queue.get_queue()

            try:

                removed, updated = queue.delete_front()

                new_steps = [
                    {
                        "items": old,
                        "message": "Original deque."
                    },
                    {
                        "items": updated,
                        "message": f"Deleted {removed} from FRONT."
                    }
                ]

                message = f"Deleted {removed} from FRONT!"

                modified = True

            except IndexError as error:

                message = str(error)

    # ==========================================
    # 13. DELETE REAR
    # ==========================================

    elif operation == "Delete Rear":

        if st.button(
            "Execute Delete Rear",
            type="primary"
        ):

            old = queue.get_queue()

            try:

                removed, updated = queue.delete_rear()

                new_steps = [
                    {
                        "items": old,
                        "message": "Original deque."
                    },
                    {
                        "items": updated,
                        "message": f"Deleted {removed} from REAR."
                    }
                ]

                message = f"Deleted {removed} from REAR!"

                modified = True

            except IndexError as error:

                message = str(error)

    # ==========================================
    # 14. IS EMPTY
    # ==========================================

    elif operation == "Is Empty":

        if st.button("Check Queue", type="primary"):

            if queue.is_empty():

                message = "Yes! The queue is empty."

            else:

                message = "No! The queue is not empty."

            new_steps = [
                {
                    "items": queue.get_queue(),
                    "message": message
                }
            ]

    # ==========================================
    # 15. IS FULL
    # ==========================================

    elif operation == "Is Full":

        if st.button("Check Queue", type="primary"):

            if queue.is_full():

                message = "Yes! The queue is full."

            else:

                message = "No! The queue is not full."

            new_steps = [
                {
                    "items": queue.get_queue(),
                    "message": message
                }
            ]

    # ==========================================
    # 16. CLEAR QUEUE
    # ==========================================

    elif operation == "Clear Queue":

        if st.button(
            "Clear Queue",
            type="primary"
        ):

            old = queue.get_queue()

            queue.clear()

            updated = queue.get_queue()

            new_steps = [
                {
                    "items": old,
                    "message": "Original queue."
                },
                {
                    "items": updated,
                    "message": "All elements removed."
                }
            ]

            message = "Queue cleared successfully!"

            modified = True

    # ==========================================
    # 17. SAVE EXECUTION RESULTS
    # ==========================================

    if new_steps:

        st.session_state.queue_steps = new_steps

        st.session_state.queue_step_index = 0

        if modified:

            st.session_state.queue_items = (
                new_steps[-1]["items"].copy()
            )

    if message:

        st.session_state.queue_message = message

    # ==========================================
    # 18. DISPLAY MESSAGE
    # ==========================================

    if st.session_state.queue_message:

        st.info(st.session_state.queue_message)

    # ==========================================
    # 19. STEP BY STEP EXECUTION
    # ==========================================

    if st.session_state.queue_steps:

        st.divider()

        st.subheader("5. Step-by-Step Execution")

        steps = st.session_state.queue_steps

        current = st.session_state.queue_step_index

        current = max(0, min(current, len(steps) - 1))

        step = steps[current]

        st.write(
            f"Step {current + 1} of {len(steps)}"
        )

        st.info(step["message"])

        step_items = step["items"]

        st.markdown("### Current Queue State")

        if step_items:

            columns = st.columns(
                min(len(step_items), 6)
            )

            for i, item in enumerate(step_items):

                with columns[i % len(columns)]:

                    if queue_type == "Priority":

                        st.metric(
                            f"Index {i}",
                            item["value"],
                            delta=f"Priority {item['priority']}"
                        )

                    else:

                        st.metric(
                            f"Index {i}",
                            item
                        )

            st.caption("FRONT → REAR")

        else:

            st.warning("Queue is empty.")

        # PREVIOUS AND NEXT BUTTONS

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "⬅ Previous Step",
                disabled=current == 0,
                use_container_width=True
            ):

                st.session_state.queue_step_index -= 1

                st.rerun()

        with col2:

            if st.button(
                "Next Step ➡",
                disabled=current == len(steps) - 1,
                use_container_width=True
            ):

                st.session_state.queue_step_index += 1

                st.rerun()

    # ==========================================
    # 20. COMPLEXITY ANALYSIS
    # ==========================================

    st.divider()

    st.subheader("6. Complexity Analysis")

    complexities = {

        "Enqueue": ("O(1)", "O(1)"),

        "Dequeue": ("O(n)", "O(1)"),

        "Peek": ("O(1)", "O(1)"),

        "Is Empty": ("O(1)", "O(1)"),

        "Is Full": ("O(1)", "O(1)"),

        "Insert Front": ("O(n)", "O(1)"),

        "Insert Rear": ("O(1)", "O(1)"),

        "Delete Front": ("O(n)", "O(1)"),

        "Delete Rear": ("O(1)", "O(1)"),

        "Clear Queue": ("O(n)", "O(1)")
    }

    time, space = complexities[operation]

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Time Complexity",
            time
        )

    with col2:

        st.metric(
            "Auxiliary Space",
            space
        )

    # ==========================================
    # END OF QUEUE VISUALIZER
    # ==========================================
