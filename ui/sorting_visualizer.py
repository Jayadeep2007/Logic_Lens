
import streamlit as st


# =====================================
# BUBBLE SORT
# =====================================
def bubble_sort(arr):
    a = arr.copy()
    steps = []
    n = len(a)

    for i in range(n):
        for j in range(n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]

            steps.append({
                "array": a.copy(),
                "current": [j, j + 1],
                "message": f"Comparing positions {j} and {j + 1}"
            })

    steps.append({
        "array": a.copy(),
        "current": [],
        "message": "Sorting completed"
    })

    return a, steps


# =====================================
# SELECTION SORT
# =====================================
def selection_sort(arr):
    a = arr.copy()
    steps = []
    n = len(a)

    for i in range(n):
        min_index = i

        for j in range(i + 1, n):
            steps.append({
                "array": a.copy(),
                "current": [min_index, j],
                "message": f"Finding minimum: comparing {a[min_index]} and {a[j]}"
            })

            if a[j] < a[min_index]:
                min_index = j

        a[i], a[min_index] = a[min_index], a[i]

        steps.append({
            "array": a.copy(),
            "current": [i],
            "message": f"Placed {a[i]} in its correct position"
        })

    steps.append({
        "array": a.copy(),
        "current": [],
        "message": "Sorting completed"
    })

    return a, steps


# =====================================
# INSERTION SORT
# =====================================
def insertion_sort(arr):
    a = arr.copy()
    steps = []

    for i in range(1, len(a)):
        key = a[i]
        j = i - 1

        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]

            steps.append({
                "array": a.copy(),
                "current": [j, j + 1],
                "message": f"Moving {a[j]} one position right"
            })

            j -= 1

        a[j + 1] = key

        steps.append({
            "array": a.copy(),
            "current": [j + 1],
            "message": f"Inserted {key} at position {j + 1}"
        })

    steps.append({
        "array": a.copy(),
        "current": [],
        "message": "Sorting completed"
    })

    return a, steps


# =====================================
# MERGE SORT
# =====================================
def merge_sort(arr):
    a = arr.copy()
    steps = []

    def divide_and_merge(left, right):
        if left >= right:
            return

        mid = (left + right) // 2

        divide_and_merge(left, mid)
        divide_and_merge(mid + 1, right)

        left_part = a[left:mid + 1]
        right_part = a[mid + 1:right + 1]

        i = 0
        j = 0
        k = left

        while i < len(left_part) and j < len(right_part):
            if left_part[i] <= right_part[j]:
                a[k] = left_part[i]
                i += 1
            else:
                a[k] = right_part[j]
                j += 1

            steps.append({
                "array": a.copy(),
                "current": [k],
                "message": f"Merging elements at position {k}"
            })
            k += 1

        while i < len(left_part):
            a[k] = left_part[i]
            i += 1

            steps.append({
                "array": a.copy(),
                "current": [k],
                "message": f"Copying remaining element to position {k}"
            })
            k += 1

        while j < len(right_part):
            a[k] = right_part[j]
            j += 1

            steps.append({
                "array": a.copy(),
                "current": [k],
                "message": f"Copying remaining element to position {k}"
            })
            k += 1

    if len(a) > 1:
        divide_and_merge(0, len(a) - 1)

    steps.append({
        "array": a.copy(),
        "current": [],
        "message": "Merge Sort completed"
    })

    return a, steps


# =====================================
# QUICK SORT
# =====================================
def quick_sort(arr):
    a = arr.copy()
    steps = []

    def partition(low, high):
        pivot = a[high]
        i = low - 1

        steps.append({
            "array": a.copy(),
            "current": [high],
            "message": f"Selected {pivot} as pivot"
        })

        for j in range(low, high):
            steps.append({
                "array": a.copy(),
                "current": [j, high],
                "message": f"Comparing {a[j]} with pivot {pivot}"
            })

            if a[j] <= pivot:
                i += 1
                a[i], a[j] = a[j], a[i]

                steps.append({
                    "array": a.copy(),
                    "current": [i, j],
                    "message": "Swapping elements"
                })

        a[i + 1], a[high] = a[high], a[i + 1]

        steps.append({
            "array": a.copy(),
            "current": [i + 1],
            "message": f"Pivot {pivot} placed in correct position"
        })

        return i + 1

    def sort(low, high):
        if low < high:
            pivot_index = partition(low, high)
            sort(low, pivot_index - 1)
            sort(pivot_index + 1, high)

    if len(a) > 1:
        sort(0, len(a) - 1)

    steps.append({
        "array": a.copy(),
        "current": [],
        "message": "Quick Sort completed"
    })

    return a, steps


# =====================================
# ARRAY DISPLAY
# =====================================
def display_array(arr, current=None):
    current = current or []

    if not arr:
        st.info("No elements to display.")
        return

    cols = st.columns(len(arr))

    for i, value in enumerate(arr):
        with cols[i]:
            st.markdown(
                f"<div style='text-align:center; font-size:12px;'>Index {i}</div>",
                unsafe_allow_html=True
            )

            if i in current:
                st.markdown(
                    f"""
                    <div style="
                        background-color:#e67e22;
                        color:white;
                        padding:15px 3px;
                        border-radius:8px;
                        text-align:center;
                        font-size:22px;
                        font-weight:bold;">
                        {value}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"""
                    <div style="
                        background-color:#2874A6;
                        color:white;
                        padding:15px 3px;
                        border-radius:8px;
                        text-align:center;
                        font-size:22px;
                        font-weight:bold;">
                        {value}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


# =====================================
# MAIN VISUALIZER
# =====================================
def render_sorting_visualizer():

    st.title("Sorting Algorithms Visualizer")

    st.write(
        "Understand how sorting algorithms arrange numbers "
        "step by step."
    )

    algorithm = st.selectbox(
        "Select Sorting Algorithm",
        [
            "Bubble Sort",
            "Selection Sort",
            "Insertion Sort",
            "Merge Sort",
            "Quick Sort"
        ],
        key="sorting_algorithm"
    )

    user_input = st.text_input(
        "Enter numbers separated by commas",
        value="50, 20, 40, 10, 30",
        key="sorting_input"
    )

    if st.button("Start Sorting", type="primary"):

        try:
            arr = [
                int(x.strip())
                for x in user_input.split(",")
                if x.strip()
            ]

            if not arr:
                st.error("Please enter at least one number.")
                return

            if len(arr) > 20:
                st.error("Please enter 20 numbers or fewer.")
                return

            if algorithm == "Bubble Sort":
                result, steps = bubble_sort(arr)

            elif algorithm == "Selection Sort":
                result, steps = selection_sort(arr)

            elif algorithm == "Insertion Sort":
                result, steps = insertion_sort(arr)

            elif algorithm == "Merge Sort":
                result, steps = merge_sort(arr)

            else:
                result, steps = quick_sort(arr)

            # Save results so they survive Streamlit reruns
            st.session_state["sort_result"] = result
            st.session_state["sort_steps"] = steps
            st.session_state["sort_original"] = arr
            st.session_state["sort_name"] = algorithm
            st.session_state["sort_step"] = 0

        except ValueError:
            st.error("Invalid input. Enter integers separated by commas.")
            return

    # =================================
    # DISPLAY SAVED RESULTS
    # =================================
    if "sort_steps" in st.session_state:

        result = st.session_state["sort_result"]
        steps = st.session_state["sort_steps"]
        original = st.session_state["sort_original"]
        selected_algorithm = st.session_state["sort_name"]

        st.divider()

        st.subheader(f"{selected_algorithm} Visualization")

        st.write("Original Array")
        display_array(original)

        st.subheader("Sorting Process")

        step_number = st.slider(
            "Move the slider to see each step",
            min_value=0,
            max_value=len(steps) - 1,
            value=st.session_state.get("sort_step", 0),
            key="sorting_step_slider"
        )

        st.session_state["sort_step"] = step_number

        current_step = steps[step_number]

        st.write(
            f"Step {step_number + 1} of {len(steps)}"
        )

        st.info(current_step["message"])

        display_array(
            current_step["array"],
            current_step["current"]
        )

        st.divider()

        st.subheader("Final Sorted Array")

        display_array(result)

        st.success("Sorting completed successfully!")

        # Complexity information
        complexity = {
            "Bubble Sort": ("O(n)", "O(n²)", "O(1)"),
            "Selection Sort": ("O(n²)", "O(n²)", "O(1)"),
            "Insertion Sort": ("O(n)", "O(n²)", "O(1)"),
            "Merge Sort": ("O(n log n)", "O(n log n)", "O(n)"),
            "Quick Sort": ("O(n log n)", "O(n²)", "O(log n) average")
        }

        best, worst, space = complexity[selected_algorithm]

        st.subheader("Time and Space Complexity")

        c1, c2, c3 = st.columns(3)

        c1.metric("Best Case", best)
        c2.metric("Worst Case", worst)
        c3.metric("Space Complexity", space)

        if st.button("Clear Visualization"):
            for key in [
                "sort_result",
                "sort_steps",
                "sort_original",
                "sort_name",
                "sort_step",
                "sorting_step_slider"
            ]:
                st.session_state.pop(key, None)

            st.rerun()
