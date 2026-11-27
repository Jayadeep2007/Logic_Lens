
import streamlit as st
import heapq
from collections import deque


# =====================================
# BUILD GRAPH
# =====================================
def build_graph(edge_text):
    graph = {}

    for line in edge_text.strip().splitlines():
        if not line.strip():
            continue

        parts = [x.strip() for x in line.split(",")]

        if len(parts) != 3:
            raise ValueError(
                "Each edge must be entered as: A,B,weight"
            )

        u, v, weight_text = parts

        if not u or not v:
            raise ValueError("Node names cannot be empty.")

        weight = float(weight_text)

        if weight < 0:
            raise ValueError("Weights cannot be negative.")

        graph.setdefault(u, {})
        graph.setdefault(v, {})

        graph[u][v] = weight
        graph[v][u] = weight

    if not graph:
        raise ValueError("Please enter at least one edge.")

    return graph


# =====================================
# BFS
# =====================================
def bfs(graph, start):
    visited = set([start])
    queue = deque([start])
    order = []
    steps = []

    while queue:
        node = queue.popleft()
        order.append(node)

        steps.append({
            "visited": order.copy(),
            "current": node,
            "message": f"Visited node {node}"
        })

        for neighbour in sorted(graph[node]):
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)

                steps.append({
                    "visited": order.copy(),
                    "current": node,
                    "message": (
                        f"Added neighbour {neighbour} "
                        f"to the queue"
                    )
                })

    return order, steps


# =====================================
# DFS
# =====================================
def dfs(graph, start):
    visited = set()
    order = []
    steps = []

    def visit(node):
        visited.add(node)
        order.append(node)

        steps.append({
            "visited": order.copy(),
            "current": node,
            "message": f"Visited node {node}"
        })

        for neighbour in sorted(graph[node]):
            if neighbour not in visited:
                steps.append({
                    "visited": order.copy(),
                    "current": node,
                    "message": (
                        f"Moving from {node} to {neighbour}"
                    )
                })
                visit(neighbour)

    visit(start)

    return order, steps


# =====================================
# DIJKSTRA
# =====================================
def dijkstra(graph, start):
    distances = {node: float("inf") for node in graph}
    distances[start] = 0

    previous = {}
    visited = set()
    heap = [(0, start)]
    steps = []

    while heap:
        distance, node = heapq.heappop(heap)

        if node in visited:
            continue

        visited.add(node)

        steps.append({
            "distances": distances.copy(),
            "current": node,
            "message": f"Processing node {node} with distance {distance}"
        })

        for neighbour, weight in sorted(graph[node].items()):
            if neighbour in visited:
                continue

            new_distance = distance + weight

            if new_distance < distances[neighbour]:
                distances[neighbour] = new_distance
                previous[neighbour] = node

                heapq.heappush(
                    heap,
                    (new_distance, neighbour)
                )

                steps.append({
                    "distances": distances.copy(),
                    "current": node,
                    "message": (
                        f"Updated distance to {neighbour}: "
                        f"{new_distance}"
                    )
                })

    return distances, previous, steps


def get_path(previous, start, target):
    path = []
    current = target

    while current != start:
        path.append(current)

        if current not in previous:
            return []

        current = previous[current]

    path.append(start)
    path.reverse()

    return path


# =====================================
# PRIM'S ALGORITHM
# =====================================
def prim(graph, start):
    visited = set([start])
    mst_edges = []
    total_weight = 0
    heap = []
    steps = []

    for neighbour, weight in graph[start].items():
        heapq.heappush(
            heap,
            (weight, start, neighbour)
        )

    while heap:
        weight, parent, node = heapq.heappop(heap)

        if node in visited:
            continue

        visited.add(node)
        mst_edges.append((parent, node, weight))
        total_weight += weight

        steps.append({
            "visited": sorted(visited),
            "edges": mst_edges.copy(),
            "total": total_weight,
            "current": node,
            "message": (
                f"Added edge {parent} - {node} "
                f"with weight {weight}"
            )
        })

        for neighbour, edge_weight in graph[node].items():
            if neighbour not in visited:
                heapq.heappush(
                    heap,
                    (edge_weight, node, neighbour)
                )

    return mst_edges, total_weight, steps, visited


# =====================================
# DISPLAY GRAPH
# =====================================
def display_graph(graph):
    st.subheader("Graph Adjacency List")

    for node in sorted(graph):
        connections = [
            f"{neighbour} ({weight:g})"
            for neighbour, weight in sorted(graph[node].items())
        ]

        st.write(f"**{node}** → " + ", ".join(connections))


# =====================================
# MAIN GRAPH VISUALIZER
# =====================================
def render_graph_visualizer():

    st.title("Graph Algorithms Visualizer")

    st.write(
        "Explore graph traversal, shortest paths "
        "and minimum spanning trees."
    )

    algorithm = st.selectbox(
        "Select Graph Algorithm",
        [
            "BFS",
            "DFS",
            "Dijkstra",
            "Prim"
        ],
        key="graph_algorithm"
    )

    edge_input = st.text_area(
        "Enter edges (one per line: Node1,Node2,Weight)",
        value="A,B,4\nA,C,2\nB,C,1\nB,D,5\nC,D,8\nC,E,10\nD,E,2",
        key="graph_edges"
    )

    try:
        graph = build_graph(edge_input)
    except ValueError as error:
        st.error(str(error))
        return

    display_graph(graph)

    start = st.selectbox(
        "Select Starting Node",
        sorted(graph.keys()),
        key="graph_start"
    )

    target = None

    if algorithm == "Dijkstra":
        target = st.selectbox(
            "Select Destination Node",
            sorted(graph.keys()),
            index=len(graph) - 1,
            key="graph_target"
        )

    if st.button("Run Algorithm", type="primary"):

        if algorithm == "BFS":
            result, steps = bfs(graph, start)

            st.session_state["graph_result"] = {
                "algorithm": algorithm,
                "order": result,
                "steps": steps
            }

        elif algorithm == "DFS":
            result, steps = dfs(graph, start)

            st.session_state["graph_result"] = {
                "algorithm": algorithm,
                "order": result,
                "steps": steps
            }

        elif algorithm == "Dijkstra":
            distances, previous, steps = dijkstra(
                graph,
                start
            )

            path = get_path(previous, start, target)

            st.session_state["graph_result"] = {
                "algorithm": algorithm,
                "distances": distances,
                "previous": previous,
                "steps": steps,
                "target": target,
                "path": path
            }

        elif algorithm == "Prim":
            edges, total, steps, visited = prim(
                graph,
                start
            )

            st.session_state["graph_result"] = {
                "algorithm": algorithm,
                "edges": edges,
                "total": total,
                "steps": steps,
                "visited": visited
            }

    # =================================
    # DISPLAY RESULTS
    # =================================
    result = st.session_state.get("graph_result")

    if result and result["algorithm"] == algorithm:

        st.divider()
        st.subheader("Algorithm Visualization")

        steps = result["steps"]

        if steps:
            step_number = st.slider(
                "Move through steps",
                min_value=0,
                max_value=len(steps) - 1,
                value=0,
                key=f"graph_slider_{algorithm}"
            )

            current_step = steps[step_number]

            st.info(current_step["message"])

            st.write(
                f"Step {step_number + 1} of {len(steps)}"
            )

            if algorithm in ["BFS", "DFS"]:
                st.write("Visited nodes:")
                st.write(current_step["visited"])

                st.write("Current node:")
                st.success(current_step["current"])

            elif algorithm == "Dijkstra":
                st.write("Current shortest distances:")

                for node, distance in current_step["distances"].items():
                    value = (
                        "∞"
                        if distance == float("inf")
                        else f"{distance:g}"
                    )

                    st.write(f"**{node}:** {value}")

                st.write("Current node:")
                st.success(current_step["current"])

            elif algorithm == "Prim":
                st.write("Visited nodes:")
                st.write(current_step["visited"])

                st.write("Selected MST edges:")

                for u, v, weight in current_step["edges"]:
                    st.write(f"{u} — {v} (weight: {weight:g})")

                st.metric(
                    "Current MST Weight",
                    f"{current_step['total']:g}"
                )

        st.divider()
        st.subheader("Final Result")

        if algorithm in ["BFS", "DFS"]:
            st.success(
                "Traversal Order: " + " → ".join(result["order"])
            )

        elif algorithm == "Dijkstra":
            st.write("Shortest distances from", start)

            for node, distance in result["distances"].items():
                if distance == float("inf"):
                    st.write(f"**{node}:** Unreachable")
                else:
                    st.write(f"**{node}:** {distance:g}")

            path = result["path"]

            if path:
                st.success(
                    f"Shortest path to {result['target']}: "
                    + " → ".join(path)
                )
                st.metric(
                    "Shortest Distance",
                    f"{result['distances'][result['target']]:g}"
                )
            else:
                st.warning(
                    f"No path exists from {start} to {result['target']}."
                )

        elif algorithm == "Prim":
            st.write("Minimum Spanning Tree Edges:")

            for u, v, weight in result["edges"]:
                st.write(f"{u} — {v} (weight: {weight:g})")

            st.metric(
                "Total MST Weight",
                f"{result['total']:g}"
            )

            if len(result["visited"]) < len(graph):
                st.warning(
                    "The graph is disconnected. "
                    "Prim's algorithm only covered the component "
                    "containing the starting node."
                )

    if st.button("Clear Graph Results"):
        st.session_state.pop("graph_result", None)
        st.rerun()
