
import streamlit as st


# =====================================
# LINEAR SEARCH
# =====================================

def linear_search(arr, target):

    steps = []
    found_index = -1

    for i in range(len(arr)):

        if arr[i] == target:
            status = "FOUND"
            found_index = i
        else:
            status = "CHECKING"

        steps.append({
            "index": i,
            "status": status,
            "message": f"Checking index {i}: Is {arr[i]} equal to {target}?"
        })

        if found_index != -1:
            break

    return found_index, steps


# =====================================
# BINARY SEARCH
# =====================================

def binary_search(arr, target):

    low = 0
    high = len(arr) - 1
    steps = []
    found_index = -1

    while low <= high:

        mid = (low + high) // 2
        value = arr[mid]

        if value == target:
            status = "FOUND"
            message = f"{value} equals {target}. Element found!"
        elif value < target:
            status = "MOVE RIGHT"
            message = f"{value} is smaller than {target}. Eliminate the left half."
        else:
            status = "MOVE LEFT"
            message = f"{value} is greater than {target}. Eliminate the right half."

        steps.append({
            "low": low,
            "mid": mid,
            "high": high,
            "value": value,
            "status": status,
            "message": message
        })

        if value == target:
            found_index = mid
            break

        elif value < target:
            low = mid + 1

        else:
            high = mid - 1

    return found_index, steps


# =====================================
# LINEAR SEARCH DISPLAY
# =====================================

def display_linear(arr, current, found):

    cols = st.columns(len(arr))

    for i, value in enumerate(arr):

        with cols[i]:

            if i == found:
                st.success(f"**{value}**")
                st.caption("FOUND")

            elif i == current:
                st.warning(f"**{value}**")
                st.caption("CHECKING")

            elif i < current:
                st.info(f"{value}")
                st.caption("CHECKED")

            else:
                st.write(f"**{value}**")
                st.caption(f"Index {i}")


# =====================================
# BINARY SEARCH DISPLAY
# =====================================

def display_binary(arr, low, mid, high, found):

    cols = st.columns(len(arr))

    for i, value in enumerate(arr):

        with cols[i]:

            if i == found:
                st.success(f"**{value}**")
                st.caption("FOUND")

            elif i == mid:
                st.warning(f"**{value}**")
                st.caption("MIDDLE")

            elif i < low or i > high:
                st.markdown(
                    f"<div style='background:#777;color:white;"
                    f"padding:10px;border-radius:8px;text-align:center;'>"
                    f"<b>{value}</b><br>ELIMINATED</div>",
                    unsafe_allow_html=True
                )

            else:
                st.info(f"**{value}**")
                st.caption("ACTIVE")


# =====================================
# MAIN VISUALIZER
# =====================================

def render_searching_visualizer():

    st.title("🔍 Searching Algorithms Visualizer")

    st.write(
        "Compare how Linear Search and Binary Search "
        "find elements in an array."
    )

    st.divider()

    algorithm = st.selectbox(
        "Choose Searching Algorithm",
        ["Linear Search", "Binary Search"]
    )

    array_input = st.text_input(
        "Enter numbers separated by commas",
        placeholder="10, 20, 30, 40, 50"
    )

    target = st.number_input(
        "Enter target value",
        value=40,
        step=1
    )

    if algorithm == "Binary Search":
        st.info(
            "Binary Search requires a sorted array."
        )

    if st.button("Run Search", type="primary"):

        try:

            arr = [
                int(x.strip())
                for x in array_input.split(",")
                if x.strip()
            ]

            if not arr:
                st.error("Enter at least one number.")

            elif len(arr) > 20:
                st.error("Enter no more than 20 numbers.")

            elif (
                algorithm == "Binary Search"
                and arr != sorted(arr)
            ):
                st.error(
                    "Please enter the array in ascending order."
                )

            else:

                if algorithm == "Linear Search":
                    index, steps = linear_search(arr, int(target))
                else:
                    index, steps = binary_search(arr, int(target))

                st.session_state.search_arr = arr
                st.session_state.search_target = int(target)
                st.session_state.search_algorithm = algorithm
                st.session_state.search_steps = steps
                st.session_state.search_index = index

                st.rerun()

        except ValueError:
            st.error("Enter valid integers separated by commas.")

    # =================================
    # VISUALIZATION
    # =================================

    if "search_arr" not in st.session_state:
        st.info("Enter an array and click Run Search.")
        return

    arr = st.session_state.search_arr
    steps = st.session_state.search_steps
    index = st.session_state.search_index
    algorithm = st.session_state.search_algorithm

    st.divider()
    st.subheader("📊 Search Visualization")

    step_number = st.slider(
        "Move through search steps",
        min_value=1,
        max_value=len(steps),
        value=1,
        key="search_visual_step"
    )

    step = steps[step_number - 1]

    st.write(f"**Step {step_number} of {len(steps)}**")

    if algorithm == "Linear Search":

        display_linear(
            arr,
            step["index"],
            index if step["status"] == "FOUND" else -1
        )

        st.warning(step["message"])

        st.caption(
            "Linear Search checks elements one after another."
        )

    else:

        display_binary(
            arr,
            step["low"],
            step["mid"],
            step["high"],
            index if step["status"] == "FOUND" else -1
        )

        st.write(f"**Low:** {step['low']}")
        st.write(f"**Middle:** {step['mid']}")
        st.write(f"**High:** {step['high']}")

        if step["status"] == "MOVE RIGHT":
            st.warning(step["message"])

        elif step["status"] == "MOVE LEFT":
            st.warning(step["message"])

        else:
            st.success(step["message"])

        st.caption(
            "Binary Search repeatedly eliminates half "
            "of the remaining search range."
        )

    # =================================
    # FINAL RESULT
    # =================================

    st.divider()
    st.subheader("🏆 Final Result")

    col1, col2 = st.columns(2)

    col1.metric("Comparisons", len(steps))
    col2.metric("Array Size", len(arr))

    if index != -1:
        st.success(
            f"Value {st.session_state.search_target} "
            f"found at index {index}!"
        )
    else:
        st.error(
            f"Value {st.session_state.search_target} not found."
        )

    # =================================
    # COMPLEXITY
    # =================================

    st.divider()
    st.subheader("⏱️ Time Complexity")

    if algorithm == "Linear Search":

        st.write("Best Case: O(1)")
        st.write("Average Case: O(n)")
        st.write("Worst Case: O(n)")

    else:

        st.write("Best Case: O(1)")
        st.write("Average Case: O(log n)")
        st.write("Worst Case: O(log n)")

    # =================================
    # CLEAR
    # =================================

    if st.button("Clear Search"):

        for key in [
            "search_arr",
            "search_target",
            "search_algorithm",
            "search_steps",
            "search_index",
            "search_visual_step"
        ]:
            st.session_state.pop(key, None)

        st.rerun()
