
import streamlit as st
import json
import os

PROFILE_FILE = "data/user_profile.json"


def load_profile():
    if os.path.exists(PROFILE_FILE):
        try:
            with open(PROFILE_FILE, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return {}

    return {}


def save_profile(profile):
    os.makedirs("data", exist_ok=True)

    with open(PROFILE_FILE, "w") as file:
        json.dump(profile, file, indent=4)


def render_profile_dashboard():

    st.title("👤 User Profile")
    st.write("Manage your LogicLens learning profile.")

    profile = load_profile()

    with st.form("profile_form"):

        st.subheader("Personal Information")

        name = st.text_input(
            "Your Name",
            value=profile.get("name", "")
        )

        email = st.text_input(
            "Email Address",
            value=profile.get("email", "")
        )

        st.subheader("Learning Preferences")

        level_options = ["Beginner", "Intermediate", "Advanced"]

        current_level = profile.get("level", "Beginner")
        level_index = (
            level_options.index(current_level)
            if current_level in level_options else 0
        )

        level = st.selectbox(
            "DSA Skill Level",
            level_options,
            index=level_index
        )

        goal = st.text_area(
            "Your Learning Goal",
            value=profile.get("goal", ""),
            placeholder="Example: Master Data Structures and Algorithms"
        )

        submitted = st.form_submit_button(
            "Save Profile",
            width="stretch"
        )

        if submitted:
            if not name.strip():
                st.error("Please enter your name.")
            else:
                new_profile = {
                    "name": name.strip(),
                    "email": email.strip(),
                    "level": level,
                    "goal": goal.strip()
                }

                save_profile(new_profile)
                st.success("Profile saved successfully!")
                st.rerun()

    st.divider()

    st.subheader("Your Profile Summary")

    profile = load_profile()

    if profile:
        st.write(f"**Name:** {profile.get('name', 'Not added')}")
        st.write(f"**Email:** {profile.get('email', 'Not added')}")
        st.write(f"**Skill Level:** {profile.get('level', 'Not selected')}")
        st.write(f"**Learning Goal:** {profile.get('goal', 'Not added')}")
    else:
        st.info("Create your profile using the form above.")
