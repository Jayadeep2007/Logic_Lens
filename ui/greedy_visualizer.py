
import streamlit as st


# =====================================
# ACTIVITY SELECTION
# =====================================
def activity_selection(activities):
    # Sort activities by finishing time
    activities = sorted(activities, key=lambda x: x[1])

    selected = []
    steps = []
    last_finish = float("-inf")

    for start, finish in activities:
        if start >= last_finish:
            selected.append((start, finish))
            last_finish = finish

            message = f"Selected activity ({start}, {finish})"
        else:
            message = f"Rejected activity ({start}, {finish}) because it overlaps"

        steps.append({
            "selected": selected.copy(),
            "message": message
        })

    return selected, steps


# =====================================
# FRACTIONAL KNAPSACK
# =====================================
def fractional_knapsack(items, capacity):
    # Each item: (name, weight, value)
    items = sorted(
        items,
        key=lambda x: x[2] / x[1],
        reverse=True
    )

    remaining = capacity
    total_value = 0
    selected = []
    steps = []

    for name, weight, value in items:
        if remaining <= 0:
            break

        fraction = min(1, remaining / weight)
        taken_weight = weight * fraction
        earned_value = value * fraction

        remaining -= taken_weight
        total_value += earned_value

        selected.append({
            "name": name,
            "fraction": fraction,
            "weight": taken_weight,
            "value": earned_value
        })

        steps.append({
            "selected": selected.copy(),
            "remaining": remaining,
            "total_value": total_value,
            "message": (
                f"Took {fraction * 100:.1f}% of {name}"
            )
        })

    return total_value, selected, steps


# =====================================
# MAIN VISUALIZER
# =====================================
def render_greedy_visualizer():

    st.title("Greedy Algorithms Visualizer")

    st.write(
        "Learn how Greedy Algorithms make the best local "
        "choice at each step."
    )

    algorithm = st.selectbox(
        "Choose Algorithm",
        [
            "Activity Selection",
            "Fractional Knapsack"
        ],
        key="greedy_algorithm"
    )

    # =================================
    # ACTIVITY SELECTION UI
    # =================================
    if algorithm == "Activity Selection":

        st.subheader("Activity Selection Problem")

        st.write(
            "Enter activities using start and finish times."
        )

        activity_input = st.text_area(
            "Enter activities (one per line: start,finish)",
            value="1,3\n2,5\n4,6\n6,8\n5,9\n8,10",
            key="activity_input"
        )

        if st.button("Find Selected Activities"):

            try:
                activities = []

                for line in activity_input.strip().splitlines():
                    start, finish = map(
                        int,
                        line.split(",")
                    )

                    if start >= finish:
                        raise ValueError

                    activities.append((start, finish))

                if not activities:
                    st.error("Enter at least one activity.")
                else:
                    selected, steps = activity_selection(activities)

                    st.session_state["activity_result"] = selected
                    st.session_state["activity_steps"] = steps

            except ValueError:
                st.error(
                    "Invalid input. Use start,finish on each line "
                    "and ensure start is smaller than finish."
                )

        if "activity_steps" in st.session_state:
            steps = st.session_state["activity_steps"]
            selected = st.session_state["activity_result"]

            st.divider()
            st.subheader("Selection Process")

            step = st.slider(
                "Explore each step",
                0,
                len(steps) - 1,
                key="activity_slider"
            )

            st.info(steps[step]["message"])

            st.write("Activities selected so far:")

            for activity in steps[step]["selected"]:
                st.success(
                    f"Start: {activity[0]} | Finish: {activity[1]}"
                )

            st.metric(
                "Maximum Activities Selected",
                len(selected)
            )

    # =================================
    # FRACTIONAL KNAPSACK UI
    # =================================
    else:

        st.subheader("Fractional Knapsack Problem")

        st.write(
            "Enter each item as name,weight,value. "
            "Weights must be greater than zero."
        )

        item_input = st.text_area(
            "Enter items (one per line: name,weight,value)",
            value="A,10,60\nB,20,100\nC,30,120",
            key="knapsack_input"
        )

        capacity = st.number_input(
            "Knapsack Capacity",
            min_value=1.0,
            value=50.0,
            step=1.0,
            key="knapsack_capacity"
        )

        if st.button("Calculate Maximum Profit"):

            try:
                items = []

                for line in item_input.strip().splitlines():
                    name, weight, value = line.split(",")

                    weight = float(weight.strip())
                    value = float(value.strip())
                    name = name.strip()

                    if not name or weight <= 0 or value < 0:
                        raise ValueError

                    items.append((name, weight, value))

                if not items:
                    st.error("Enter at least one item.")
                else:
                    total, selected, steps = fractional_knapsack(
                        items,
                        capacity
                    )

                    st.session_state["knapsack_total"] = total
                    st.session_state["knapsack_selected"] = selected
                    st.session_state["knapsack_steps"] = steps

            except ValueError:
                st.error(
                    "Invalid input. Use name,weight,value. "
                    "Weight must be positive and value cannot be negative."
                )

        if "knapsack_steps" in st.session_state:
            steps = st.session_state["knapsack_steps"]
            selected = st.session_state["knapsack_selected"]
            total = st.session_state["knapsack_total"]

            st.divider()
            st.subheader("Knapsack Selection Process")

            step = st.slider(
                "Explore each step",
                0,
                len(steps) - 1,
                key="knapsack_slider"
            )

            current = steps[step]

            st.info(current["message"])

            st.write("Items selected so far:")

            for item in current["selected"]:
                st.success(
                    f"{item['name']}: "
                    f"{item['fraction'] * 100:.1f}% selected | "
                    f"Weight: {item['weight']:.2f} | "
                    f"Value: {item['value']:.2f}"
                )

            st.metric(
                "Current Total Value",
                f"{current['total_value']:.2f}"
            )

            st.metric(
                "Remaining Capacity",
                f"{current['remaining']:.2f}"
            )

            st.divider()

            st.subheader("Final Result")

            st.metric("Maximum Profit", f"{total:.2f}")

            st.write(
                f"Total weight used: "
                f"{sum(item['weight'] for item in selected):.2f}"
            )
