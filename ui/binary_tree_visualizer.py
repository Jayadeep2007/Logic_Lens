
# ==========================================
# LOGICLENS - BINARY TREE VISUALIZER
# ==========================================

import streamlit as st
from collections import deque


# ==========================================
# NODE CLASS
# ==========================================

class Node:

    def __init__(self, value):

        self.value = value
        self.left = None
        self.right = None


# ==========================================
# BUILD TREE FROM LEVEL ORDER INPUT
# ==========================================

def build_tree(values):

    if not values or values[0] is None:
        return None

    root = Node(values[0])

    queue = deque([root])

    index = 1

    while queue and index < len(values):

        current = queue.popleft()

        if index < len(values):

            if values[index] is not None:

                current.left = Node(values[index])
                queue.append(current.left)

            index += 1

        if index < len(values):

            if values[index] is not None:

                current.right = Node(values[index])
                queue.append(current.right)

            index += 1

    return root


# ==========================================
# INSERT NODE - LEVEL ORDER
# ==========================================

def insert_node(root, value):

    new_node = Node(value)

    if root is None:
        return new_node

    queue = deque([root])

    while queue:

        current = queue.popleft()

        if current.left is None:

            current.left = new_node
            return root

        else:
            queue.append(current.left)

        if current.right is None:

            current.right = new_node
            return root

        else:
            queue.append(current.right)

    return root


# ==========================================
# DELETE NODE
# ==========================================

def delete_node(root, value):

    if root is None:
        return None, False

    if root.left is None and root.right is None:

        if root.value == value:
            return None, True

        return root, False

    queue = deque([(root, None)])

    target = None
    deepest = None
    deepest_parent = None

    while queue:

        current, parent = queue.popleft()

        if current.value == value and target is None:
            target = current

        deepest = current
        deepest_parent = parent

        if current.left:
            queue.append((current.left, current))

        if current.right:
            queue.append((current.right, current))

    if target is None:
        return root, False

    target.value = deepest.value

    if deepest_parent.left is deepest:
        deepest_parent.left = None

    else:
        deepest_parent.right = None

    return root, True


# ==========================================
# PREORDER TRAVERSAL
# ==========================================

def preorder(root):

    result = []

    def traverse(node):

        if node is None:
            return

        result.append(node.value)

        traverse(node.left)

        traverse(node.right)

    traverse(root)

    return result


# ==========================================
# INORDER TRAVERSAL
# ==========================================

def inorder(root):

    result = []

    def traverse(node):

        if node is None:
            return

        traverse(node.left)

        result.append(node.value)

        traverse(node.right)

    traverse(root)

    return result


# ==========================================
# POSTORDER TRAVERSAL
# ==========================================

def postorder(root):

    result = []

    def traverse(node):

        if node is None:
            return

        traverse(node.left)

        traverse(node.right)

        result.append(node.value)

    traverse(root)

    return result


# ==========================================
# LEVEL ORDER TRAVERSAL
# ==========================================

def level_order(root):

    result = []

    if root is None:
        return result

    queue = deque([root])

    while queue:

        current = queue.popleft()

        result.append(current.value)

        if current.left:
            queue.append(current.left)

        if current.right:
            queue.append(current.right)

    return result


# ==========================================
# TREE HEIGHT
# Height is measured in number of nodes.
# ==========================================

def tree_height(root):

    if root is None:
        return 0

    left_height = tree_height(root.left)

    right_height = tree_height(root.right)

    return 1 + max(left_height, right_height)


# ==========================================
# COUNT TOTAL NODES
# ==========================================

def count_nodes(root):

    if root is None:
        return 0

    return (
        1
        + count_nodes(root.left)
        + count_nodes(root.right)
    )


# ==========================================
# COUNT LEAF NODES
# ==========================================

def count_leaf_nodes(root):

    if root is None:
        return 0

    if root.left is None and root.right is None:
        return 1

    return (
        count_leaf_nodes(root.left)
        + count_leaf_nodes(root.right)
    )


# ==========================================
# GENERATE GRAPHVIZ TREE
# ==========================================

def generate_tree_graph(root):

    lines = [
        "digraph BinaryTree {",
        'graph [rankdir=TB, bgcolor="transparent"];',
        'node [shape=circle, style=filled, '
        'fillcolor="#1D4ED8", fontcolor="white", '
        'color="#60A5FA", penwidth=2];',
        'edge [color="#94A3B8", penwidth=2];'
    ]

    def add_edges(node, node_id):

        if node is None:
            return

        if node.left:

            left_id = node_id + "L"

            lines.append(
                f'"{node_id}" -> "{left_id}";'
            )

            lines.append(
                f'"{left_id}" [label="{node.left.value}"];'
            )

            add_edges(node.left, left_id)

        if node.right:

            right_id = node_id + "R"

            lines.append(
                f'"{node_id}" -> "{right_id}";'
            )

            lines.append(
                f'"{right_id}" [label="{node.right.value}"];'
            )

            add_edges(node.right, right_id)

    if root is not None:

        lines.append(
            f'"root" [label="{root.value}"];'
        )

        add_edges(root, "root")

    lines.append("}")

    return "\n".join(lines)


# ==========================================
# MAIN VISUALIZER
# ==========================================

def render_binary_tree_visualizer():

    st.title("🌳 Binary Tree Visualizer")

    st.write(
        "Create, modify and explore Binary Trees "
        "using interactive operations and traversals."
    )

    st.divider()

    # SESSION STATE

    if "binary_tree_root" not in st.session_state:
        st.session_state.binary_tree_root = None

    if "binary_tree_message" not in st.session_state:
        st.session_state.binary_tree_message = ""

    root = st.session_state.binary_tree_root

    # ======================================
    # 1. CREATE TREE
    # ======================================

    st.subheader("1. Create Binary Tree")

    st.write(
        "Enter values in level order, separated by commas. "
        "Use None for an empty child position."
    )

    tree_input = st.text_input(
        "Enter tree values",
        placeholder="10, 20, 30, 40, 50, None, 60",
        key="binary_tree_input"
    )

    if st.button("Create Tree", type="primary"):

        try:

            values = []

            if tree_input.strip():

                for value in tree_input.split(","):

                    value = value.strip()

                    if value.lower() in ["none", "null", "#", ""]:
                        values.append(None)

                    else:
                        values.append(int(value))

            else:
                raise ValueError("Please enter tree values.")

            if not values or values[0] is None:
                raise ValueError("The root cannot be empty.")

            root = build_tree(values)

            st.session_state.binary_tree_root = root

            st.session_state.binary_tree_message = (
                "Binary Tree created successfully!"
            )

        except ValueError as error:

            st.session_state.binary_tree_message = str(error)

        st.rerun()

    root = st.session_state.binary_tree_root

    # ======================================
    # 2. INSERT AND DELETE
    # ======================================

    st.divider()

    st.subheader("2. Tree Operations")

    col1, col2 = st.columns(2)

    with col1:

        insert_value = st.number_input(
            "Value to Insert",
            value=70,
            step=1,
            key="binary_insert_value"
        )

        if st.button("➕ Insert Node", use_container_width=True):

            root = insert_node(
                st.session_state.binary_tree_root,
                int(insert_value)
            )

            st.session_state.binary_tree_root = root

            st.session_state.binary_tree_message = (
                f"Inserted {insert_value} successfully!"
            )

            st.rerun()

    with col2:

        delete_value = st.number_input(
            "Value to Delete",
            value=10,
            step=1,
            key="binary_delete_value"
        )

        if st.button("➖ Delete Node", use_container_width=True):

            root, deleted = delete_node(
                st.session_state.binary_tree_root,
                int(delete_value)
            )

            st.session_state.binary_tree_root = root

            if deleted:

                st.session_state.binary_tree_message = (
                    f"Deleted {delete_value} successfully!"
                )

            else:

                st.session_state.binary_tree_message = (
                    f"Value {delete_value} not found."
                )

            st.rerun()

    if st.session_state.binary_tree_message:

        st.info(st.session_state.binary_tree_message)

    # ======================================
    # 3. VISUALIZATION
    # ======================================

    st.divider()

    st.subheader("3. Binary Tree Visualization")

    root = st.session_state.binary_tree_root

    if root is None:

        st.warning("Create a tree to see the visualization.")

    else:

        graph = generate_tree_graph(root)

        st.graphviz_chart(
            graph,
            use_container_width=True
        )

    # ======================================
    # 4. TRAVERSALS
    # ======================================

    st.divider()

    st.subheader("4. Tree Traversals")

    traversal = st.selectbox(
        "Choose Traversal",
        [
            "Preorder",
            "Inorder",
            "Postorder",
            "Level Order"
        ]
    )

    if st.button("Execute Traversal", type="primary"):

        root = st.session_state.binary_tree_root

        if root is None:

            st.warning("Please create a tree first.")

        else:

            if traversal == "Preorder":
                result = preorder(root)

            elif traversal == "Inorder":
                result = inorder(root)

            elif traversal == "Postorder":
                result = postorder(root)

            else:
                result = level_order(root)

            st.success(
                f"{traversal} Traversal: "
                + " → ".join(map(str, result))
            )

    # ======================================
    # 5. TREE INFORMATION
    # ======================================

    st.divider()

    st.subheader("5. Tree Analysis")

    root = st.session_state.binary_tree_root

    if root is not None:

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Total Nodes",
                count_nodes(root)
            )

        with col2:

            st.metric(
                "Tree Height",
                tree_height(root)
            )

        with col3:

            st.metric(
                "Leaf Nodes",
                count_leaf_nodes(root)
            )

        st.write("**Preorder:**", preorder(root))

        st.write("**Inorder:**", inorder(root))

        st.write("**Postorder:**", postorder(root))

        st.write("**Level Order:**", level_order(root))

    else:

        st.info("Tree analysis will appear after creating a tree.")

    # ======================================
    # 6. COMPLEXITY ANALYSIS
    # ======================================

    st.divider()

    st.subheader("6. Complexity Analysis")

    complexity_data = {
        "Preorder Traversal": "O(n)",
        "Inorder Traversal": "O(n)",
        "Postorder Traversal": "O(n)",
        "Level Order Traversal": "O(n)",
        "Insert Node": "O(n)",
        "Delete Node": "O(n)",
        "Tree Height": "O(n)",
        "Count Nodes": "O(n)",
        "Count Leaf Nodes": "O(n)"
    }

    for operation, complexity in complexity_data.items():

        st.write(
            f"**{operation}:** {complexity}"
        )

    # ======================================
    # 7. RESET TREE
    # ======================================

    st.divider()

    if st.button("🗑️ Clear Entire Tree"):

        st.session_state.binary_tree_root = None

        st.session_state.binary_tree_message = (
            "Binary Tree cleared successfully!"
        )

        st.rerun()
