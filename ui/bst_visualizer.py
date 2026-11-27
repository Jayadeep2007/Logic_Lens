
# ==========================================
# LOGICLENS - BINARY SEARCH TREE VISUALIZER
# ==========================================

import streamlit as st


# ==========================================
# NODE CLASS
# ==========================================

class Node:

    def __init__(self, value):

        self.value = value
        self.left = None
        self.right = None


# ==========================================
# INSERT NODE
# ==========================================

def insert_node(root, value):

    if root is None:
        return Node(value)

    if value < root.value:

        root.left = insert_node(root.left, value)

    elif value > root.value:

        root.right = insert_node(root.right, value)

    # Duplicate values are ignored.
    return root


# ==========================================
# SEARCH NODE
# ==========================================

def search_node(root, value):

    current = root
    path = []

    while current is not None:

        path.append(current.value)

        if value == current.value:
            return True, path

        elif value < current.value:
            current = current.left

        else:
            current = current.right

    return False, path


# ==========================================
# FIND MINIMUM NODE
# ==========================================

def find_minimum(root):

    if root is None:
        return None

    current = root

    while current.left is not None:
        current = current.left

    return current.value


# ==========================================
# FIND MAXIMUM NODE
# ==========================================

def find_maximum(root):

    if root is None:
        return None

    current = root

    while current.right is not None:
        current = current.right

    return current.value


# ==========================================
# DELETE NODE
# ==========================================

def delete_node(root, value):

    if root is None:
        return None, False

    if value < root.value:

        root.left, deleted = delete_node(
            root.left, value
        )

    elif value > root.value:

        root.right, deleted = delete_node(
            root.right, value
        )

    else:

        # Case 1: No child
        if root.left is None and root.right is None:
            return None, True

        # Case 2: Only right child
        if root.left is None:
            return root.right, True

        # Case 3: Only left child
        if root.right is None:
            return root.left, True

        # Case 4: Two children
        successor_value = find_minimum(root.right)

        root.value = successor_value

        root.right, _ = delete_node(
            root.right, successor_value
        )

        return root, True

    return root, deleted


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
# TREE HEIGHT
# ==========================================

def tree_height(root):

    if root is None:
        return 0

    return 1 + max(
        tree_height(root.left),
        tree_height(root.right)
    )


# ==========================================
# COUNT NODES
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
# GENERATE GRAPHVIZ TREE
# ==========================================

def generate_bst_graph(root):

    lines = [
        "digraph BST {",
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
                f'"{node_id}" -> "{left_id}" '
                '[label="L"];'
            )

            lines.append(
                f'"{left_id}" [label="{node.left.value}"];'
            )

            add_edges(node.left, left_id)

        if node.right:

            right_id = node_id + "R"

            lines.append(
                f'"{node_id}" -> "{right_id}" '
                '[label="R"];'
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
# MAIN BST VISUALIZER
# ==========================================

def render_bst_visualizer():

    st.title("🌳 Binary Search Tree Visualizer")

    st.write(
        "Explore how Binary Search Trees work "
        "through interactive insertion, deletion and searching."
    )

    st.divider()

    # ======================================
    # SESSION STATE
    # ======================================

    if "bst_root" not in st.session_state:
        st.session_state.bst_root = None

    if "bst_message" not in st.session_state:
        st.session_state.bst_message = ""

    if "bst_search_path" not in st.session_state:
        st.session_state.bst_search_path = []

    root = st.session_state.bst_root

    # ======================================
    # CREATE BST
    # ======================================

    st.subheader("1. Create Your BST")

    with st.form("bst_creation_form"):

        user_input = st.text_input(
            "Enter values separated by commas",
            placeholder="50, 30, 70, 20, 40, 60, 80"
        )

        create_button = st.form_submit_button(
            "Create BST",
            type="primary"
        )

        if create_button:

            try:

                values = [
                    int(value.strip())
                    for value in user_input.split(",")
                    if value.strip()
                ]

                if not values:
                    st.error("Enter at least one value.")

                elif len(values) > 100:
                    st.error("Maximum 100 values allowed.")

                else:

                    root = None

                    for value in values:
                        root = insert_node(root, value)

                    st.session_state.bst_root = root
                    st.session_state.bst_search_path = []

                    st.session_state.bst_message = (
                        "BST created successfully!"
                    )

                    st.rerun()

            except ValueError:

                st.error("Enter valid integer values.")

    # ======================================
    # INSERT AND DELETE
    # ======================================

    st.divider()

    st.subheader("2. BST Operations")

    col1, col2 = st.columns(2)

    with col1:

        insert_value = st.number_input(
            "Value to Insert",
            value=25,
            step=1,
            key="bst_insert_value"
        )

        if st.button(
            "➕ Insert Node",
            use_container_width=True
        ):

            old_count = count_nodes(
                st.session_state.bst_root
            )

            new_root = insert_node(
                st.session_state.bst_root,
                int(insert_value)
            )

            new_count = count_nodes(new_root)

            st.session_state.bst_root = new_root

            st.session_state.bst_search_path = []

            if new_count > old_count:

                st.session_state.bst_message = (
                    f"Inserted {insert_value} successfully!"
                )

            else:

                st.session_state.bst_message = (
                    "Duplicate value! BST does not allow duplicates."
                )

            st.rerun()

    with col2:

        delete_value = st.number_input(
            "Value to Delete",
            value=20,
            step=1,
            key="bst_delete_value"
        )

        if st.button(
            "➖ Delete Node",
            use_container_width=True
        ):

            new_root, deleted = delete_node(
                st.session_state.bst_root,
                int(delete_value)
            )

            st.session_state.bst_root = new_root

            st.session_state.bst_search_path = []

            if deleted:

                st.session_state.bst_message = (
                    f"Deleted {delete_value} successfully!"
                )

            else:

                st.session_state.bst_message = (
                    f"{delete_value} was not found."
                )

            st.rerun()

    if st.session_state.bst_message:

        st.info(st.session_state.bst_message)

    # ======================================
    # SEARCH
    # ======================================

    st.divider()

    st.subheader("3. Search a Node")

    search_value = st.number_input(
        "Enter value to search",
        value=50,
        step=1,
        key="bst_search_value"
    )

    if st.button(
        "🔍 Search Node",
        type="primary"
    ):

        found, path = search_node(
            st.session_state.bst_root,
            int(search_value)
        )

        st.session_state.bst_search_path = path

        if found:

            st.success(
                f"{search_value} found in the BST!"
            )

        else:

            st.error(
                f"{search_value} not found in the BST."
            )

        if path:

            st.write(
                "Search path: "
                + " → ".join(map(str, path))
            )

    # ======================================
    # TREE VISUALIZATION
    # ======================================

    st.divider()

    st.subheader("4. BST Visualization")

    root = st.session_state.bst_root

    if root is None:

        st.warning("Create a BST to see its visualization.")

    else:

        col1, col2, col3 = st.columns([1, 3, 1])

        with col2:
             st.graphviz_chart(
            generate_bst_graph(root),
            width="content"
    )

    # ======================================
    # TRAVERSALS
    # ======================================

    st.divider()

    st.subheader("5. Tree Traversals")

    traversal = st.selectbox(
        "Select Traversal",
        [
            "Inorder",
            "Preorder",
            "Postorder"
        ]
    )

    if st.button(
        "Execute Traversal",
        type="primary"
    ):

        root = st.session_state.bst_root

        if root is None:

            st.warning("Please create a BST first.")

        else:

            if traversal == "Inorder":
                result = inorder(root)

            elif traversal == "Preorder":
                result = preorder(root)

            else:
                result = postorder(root)

            st.success(
                traversal + ": "
                + " → ".join(map(str, result))
            )

    # ======================================
    # MINIMUM AND MAXIMUM
    # ======================================

    st.divider()

    st.subheader("6. Minimum and Maximum")

    root = st.session_state.bst_root

    col1, col2 = st.columns(2)

    with col1:

        minimum = find_minimum(root)

        st.metric(
            "Minimum Value",
            str(minimum) if minimum is not None else "Empty"
        )

    with col2:

        maximum = find_maximum(root)

        st.metric(
            "Maximum Value",
            str(maximum) if maximum is not None else "Empty"
        )

    # ======================================
    # TREE ANALYSIS
    # ======================================

    st.divider()

    st.subheader("7. BST Analysis")

    root = st.session_state.bst_root

    col1, col2 = st.columns(2)

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

    if root is not None:

        st.write("**Sorted Elements:**", inorder(root))

    # ======================================
    # COMPLEXITY ANALYSIS
    # ======================================

    st.divider()

    st.subheader("8. Complexity Analysis")

    complexity = {
        "Insertion": "O(h)",
        "Deletion": "O(h)",
        "Searching": "O(h)",
        "Minimum": "O(h)",
        "Maximum": "O(h)",
        "Inorder Traversal": "O(n)",
        "Preorder Traversal": "O(n)",
        "Postorder Traversal": "O(n)",
        "Tree Height": "O(n)",
        "Count Nodes": "O(n)"
    }

    for operation, value in complexity.items():

        st.write(f"**{operation}:** {value}")

    st.caption(
        "h = tree height. A balanced BST has O(log n) "
        "search, insertion and deletion; a skewed BST "
        "can take O(n)."
    )

    # ======================================
    # CLEAR BST
    # ======================================

    st.divider()

    if st.button("🗑️ Clear Entire BST"):

        st.session_state.bst_root = None
        st.session_state.bst_search_path = []

        st.session_state.bst_message = (
            "BST cleared successfully!"
        )

        st.rerun()
