
import streamlit as st
import importlib

from ui.code_playground import render_code_playground
from ui.quiz_visualizer import render_quiz_visualizer
from ui.progress_dashboard import render_progress_dashboard
from ui.progress_dashboard import record_quiz_result
from ui.profile_dashboard import render_profile_dashboard
# ==================================================
# 1. PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="LogicLens | DSA Learning",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# 2. SESSION STATE
# ==================================================

if "navigation" not in st.session_state:
    st.session_state["navigation"] = "Dashboard"

if "selected_dsa_module" not in st.session_state:
    st.session_state["selected_dsa_module"] = "Array"


# ==================================================
# 3. CUSTOM CSS
# ==================================================

st.markdown("""
<style>

.stApp {
    background-color: #0B0F19;
    color: #F8FAFC;
}

#MainMenu, footer {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #29344B;
}

h1, h2, h3 {
    color: #F8FAFC !important;
}

p {
    color: #CBD5E1;
}

.stButton > button {
    background: linear-gradient(90deg, #7C3AED, #2563EB);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    transition: all 0.25s ease;
}

.stButton > button:hover {
    border: 1px solid #A78BFA;
    color: white;
    transform: translateY(-3px);
    box-shadow: 0 5px 20px rgba(124, 58, 237, 0.25);
}

.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    background-color: #171F31;
    color: white;
    border: 1px solid #34415B;
    border-radius: 8px;
}

div[data-baseweb="select"] > div {
    background-color: #171F31;
    border-color: #34415B;
}

.hero {
    background: linear-gradient(120deg, #25164A, #172554, #111827);
    border: 1px solid #37306B;
    border-radius: 20px;
    padding: 38px;
    margin-bottom: 28px;
}

.hero-title {
    font-size: 40px;
    font-weight: 800;
    color: white;
    line-height: 1.2;
    margin-top: 12px;
}

.hero-description {
    color: #C4B5FD;
    font-size: 16px;
    margin-top: 15px;
    max-width: 700px;
}

.section-label {
    color: #A78BFA;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
}

.logic-card {
    background: linear-gradient(145deg, #1B2540, #111827);
    border: 1px solid #29344B;
    border-radius: 16px;
    padding: 24px;
    min-height: 145px;
    margin-bottom: 10px;
    transition: all 0.3s ease;
}

.logic-card:hover {
    transform: translateY(-5px);
    border-color: #8B5CF6;
    box-shadow: 0 10px 30px rgba(124, 58, 237, 0.18);
}

.card-icon {
    font-size: 30px;
    margin-bottom: 12px;
}

.card-title {
    font-size: 19px;
    font-weight: 700;
    color: #F8FAFC;
    margin-bottom: 8px;
}

.card-description {
    font-size: 13px;
    color: #94A3B8;
}

div[data-testid="stMetric"] {
    background-color: #171F31;
    border: 1px solid #29344B;
    padding: 15px;
    border-radius: 12px;
}

hr {
    border-color: #29344B;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# 4. NAVIGATION FUNCTIONS
# ==================================================

def open_visualizer(module_name):
    st.session_state["selected_dsa_module"] = module_name
    st.session_state["navigation"] = "DSA Visualizers"


def open_page(page_name):
    st.session_state["navigation"] = page_name


# ==================================================
# 5. SIDEBAR
# ==================================================

with st.sidebar:

    st.html("""
    <div style="padding:12px 5px 20px 5px;">
        <div style="
            font-size:30px;
            font-weight:800;
            color:#A78BFA;">
            🧠 LogicLens
        </div>
        <div style="
            color:#94A3B8;
            font-size:12px;
            letter-spacing:1px;">
            DSA LEARNING PLATFORM
        </div>
    </div>
    """)

    st.divider()

    st.markdown("### NAVIGATION")

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "DSA Visualizers",
            "DSA Quiz",
            "Learning Progress",
            "Code Playground",
            "Learn DSA",
            "User Profile",
            "About"
        ],
        key="navigation",
        label_visibility="collapsed"
    )

    st.divider()

    st.html("""
    <div style="
        background:#1C2540;
        border-radius:12px;
        padding:15px;">
        <div style="color:#A78BFA;font-weight:700;">
            💡 Learning Tip
        </div>
        <div style="
            color:#CBD5E1;
            font-size:13px;
            margin-top:8px;">
            Practice one algorithm every day.
            Understand the logic before memorizing the code.
        </div>
    </div>
    <div style="
        color:#64748B;
        font-size:11px;
        margin-top:35px;">
        LogicLens v1.0
    </div>
    """)


# ==================================================
# 6. TOP HEADER
# ==================================================

st.html("""
<div style="
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-bottom:20px;">

    <div>
        <div style="font-size:13px;color:#94A3B8;">
            LEARN • VISUALIZE • MASTER
        </div>
        <div style="
            font-size:24px;
            font-weight:750;
            color:#F8FAFC;">
            Welcome to LogicLens
        </div>
    </div>

    <div style="
        background:#1E293B;
        color:#A78BFA;
        border:1px solid #37306B;
        border-radius:30px;
        padding:9px 16px;
        font-size:12px;">
        ✦ DSA Learning
    </div>
</div>
""")


# ==================================================
# 7. DASHBOARD
# ==================================================

def show_dashboard():

    st.html("""
    <div class="hero">
        <div class="section-label">
            YOUR DSA JOURNEY STARTS HERE
        </div>

        <div class="hero-title">
            Think Better.<br>Code Smarter.
        </div>

        <div class="hero-description">
            Understand Data Structures and Algorithms
            through interactive visualizations and
            hands-on learning.
        </div>
    </div>
    """)

    col1, col2, col3 = st.columns(3)

    col1.metric("DSA Modules", "12", "Interactive learning")
    col2.metric("Learning Paths", "4", "Explore and practice")
    col3.metric("Platform", "LogicLens", "Version 1.0")

    st.divider()

    st.markdown("### 🚀 Explore Your Learning Space")

    cards = [
        ("🧩", "Data Structures",
         "Explore Arrays, Linked Lists, Stacks and Queues.",
         "Array"),

        ("⚡", "Algorithms",
         "Explore Searching, Sorting and Greedy Algorithms.",
         "Sorting Algorithms"),

        ("🌐", "Graph Algorithms",
         "Explore BFS, DFS, Dijkstra and Prim.",
         "Graph Algorithms"),

        ("🌳", "Binary Tree",
         "Understand tree structures and operations.",
         "Binary Tree"),

        ("📚", "Stack",
         "Learn LIFO operations step by step.",
         "Stack"),

        ("🚦", "Queue",
         "Understand FIFO operations.",
         "Queue"),

        ("🔗", "Linked List",
         "Explore linked list operations.",
         "Linked List"),

        ("🔍", "Searching",
         "Learn Linear and Binary Search.",
         "Searching Algorithms"),

        ("🧠", "Dynamic Programming",
         "Explore Fibonacci, Knapsack and LCS.",
         "Dynamic Programming"),

        ("🎯", "Greedy Algorithms",
         "Learn Activity Selection and Knapsack.",
         "Greedy Algorithms")
    ]

    # Cards displayed in two columns

    for start in range(0, len(cards), 2):

        columns = st.columns(2)

        for col, card in zip(columns, cards[start:start + 2]):

            with col:

                icon, title, description, module = card

                # Render actual HTML instead of Markdown code blocks
                st.html(f"""
                <div class="logic-card">
                    <div class="card-icon">{icon}</div>
                    <div class="card-title">{title}</div>
                    <div class="card-description">{description}</div>
                </div>
                """)

                # Real clickable Streamlit button
                st.button(
                    f"Explore {title}",
                    key=f"dashboard_{module}",
                    on_click=open_visualizer,
                    args=(module,),
                    use_container_width=True
                )

    st.divider()

    st.markdown("### 💻 More Learning Options")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### Code Playground")
        st.write("Practice Python programming.")

        st.button(
            "Open Playground",
            key="open_playground",
            on_click=open_page,
            args=("Code Playground",),
            use_container_width=True
        )

    with col2:
        st.markdown("#### Learn DSA")
        st.write("Understand concepts and complexity.")

        st.button(
            "Start Learning",
            key="open_learning",
            on_click=open_page,
            args=("Learn DSA",),
            use_container_width=True
        )

    with col3:
        st.markdown("#### About LogicLens")
        st.write("Learn about this platform.")

        st.button(
            "About Us",
            key="open_about",
            on_click=open_page,
            args=("About",),
            use_container_width=True
        )

    st.divider()

    st.markdown("### ✨ Why LogicLens?")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Visual Learning**

        Understand how algorithms work through
        step-by-step execution.
        """)

    with col2:
        st.markdown("""
        **Practical Understanding**

        Experiment with different inputs and
        observe the results.
        """)


# ==================================================
# 8. DSA VISUALIZERS
# ==================================================

def show_dsa_visualizers():

    st.title("🧩 DSA Visualizers")

    st.write(
        "Choose a topic to explore its interactive visualizer."
    )

    visualizers = {

        "Array": (
            "ui.dsa_visualizer",
            "render_array_visualizer"
        ),

        "Linked List": (
            "ui.linked_list_visualizer",
            "render_linked_list_visualizer"
        ),

        "Stack": (
            "ui.stack_visualizer",
            "render_stack_visualizer"
        ),

        "Queue": (
            "ui.queue_visualizer",
            "render_queue_visualizer"
        ),

        "Binary Tree": (
            "ui.binary_tree_visualizer",
            "render_binary_tree_visualizer"
        ),

        "Binary Search Tree": (
            "ui.bst_visualizer",
            "render_bst_visualizer"
        ),

        "Recursion": (
            "ui.recursion_visualizer",
            "render_recursion_visualizer"
        ),

        "Searching Algorithms": (
            "ui.searching_visualizer",
            "render_searching_visualizer"
        ),

        "Sorting Algorithms": (
            "ui.sorting_visualizer",
            "render_sorting_visualizer"
        ),

        "Greedy Algorithms": (
            "ui.greedy_visualizer",
            "render_greedy_visualizer"
        ),

        "Dynamic Programming": (
            "ui.dynamic_programming_visualizer",
            "render_dynamic_programming_visualizer"
        ),

        "Graph Algorithms": (
            "ui.graph_visualizer",
            "render_graph_visualizer"
        )
    }

    selected = st.selectbox(
        "Choose DSA Module",
        list(visualizers.keys()),
        key="selected_dsa_module"
    )

    st.divider()

    module_path, function_name = visualizers[selected]

    try:

        module = importlib.import_module(module_path)

        render_function = getattr(module, function_name)

        render_function()

    except ModuleNotFoundError as error:

        st.error(f"Module not found: {module_path}")
        st.code(str(error))

    except AttributeError as error:

        st.error(
            f"Function {function_name} was not found "
            f"inside {module_path}."
        )
        st.code(str(error))

    except Exception as error:

        st.error("An error occurred while loading the visualizer.")
        st.exception(error)


# ==================================================
# 9. CODE PLAYGROUND
# ==================================================

def show_code_playground():
    render_code_playground()

    st.title("💻 Code Playground")

    st.write("Write and experiment with Python programs.")

    st.info(
        "The code execution feature will be added in the next phase."
    )

    st.text_area(
        "Python Code",
        value="# Welcome to LogicLens!\n\nprint('Hello, LogicLens!')",
        height=250
    )

    st.caption("Code execution is not enabled yet.")


# ==================================================
# 10. LEARN DSA
# ==================================================

def show_learn_dsa():

    st.title("📚 Learn DSA")

    st.write(
        "Build your knowledge of Data Structures and Algorithms."
    )

    topics = {
        "Introduction to DSA":
            "Learn what Data Structures and Algorithms are.",

        "Time Complexity":
            "Understand Big O notation and algorithm efficiency.",

        "Arrays":
            "Learn indexing, insertion, deletion and traversal.",

        "Linked Lists":
            "Understand nodes, links and linked list operations.",

        "Stacks and Queues":
            "Learn LIFO and FIFO data structures.",

        "Searching and Sorting":
            "Explore common searching and sorting techniques.",

        "Trees and Graphs":
            "Understand hierarchical and network-based structures.",

        "Greedy Algorithms":
            "Learn how greedy algorithms make local choices.",

        "Dynamic Programming":
            "Understand overlapping subproblems and optimal substructure."
    }

    for topic, description in topics.items():
        with st.expander(topic):
            st.write(description)


# ==================================================
# 11. ABOUT
# ==================================================

def show_about():

    st.title("🧠 About LogicLens")

    st.markdown("""
    **LogicLens** is an interactive Data Structures
    and Algorithms learning platform.

    ### Our Goal

    To make learning DSA easier through visualization,
    practical examples and step-by-step explanations.

    ### Platform Features

    - Interactive data structure visualizers
    - Algorithm demonstrations
    - Step-by-step learning
    - Complexity explanations
    - Practical coding environment (planned)

    ### Our Motto

    **Think Better. Code Smarter.**
    """)


# ==================================================
# 12. PAGE ROUTING
# ==================================================

if page == "Dashboard":
    show_dashboard()

elif page == "DSA Visualizers":
    show_dsa_visualizers()

elif page == "Code Playground":
    show_code_playground()

elif page == "Learn DSA":
    show_learn_dsa()

elif page == "About":
    show_about()

elif page == "DSA Quiz":
    render_quiz_visualizer()

elif page == "Learning Progress":
    render_progress_dashboard()
    
elif page == "User Profile":
    render_profile_dashboard()


# ==================================================
# 13. FOOTER
# ==================================================

st.html("""
<div style="
    text-align:center;
    color:#64748B;
    font-size:12px;
    padding:15px;">
    🧠 LogicLens | Think Better. Code Smarter.
</div>
""")
