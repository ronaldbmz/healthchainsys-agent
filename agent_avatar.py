import streamlit as st
import json
import os

# Load avatar profile
def load_profile():
    profile_path = "core/agents/discern/profile.json"
    if os.path.exists(profile_path):
        with open(profile_path, "r") as file:
            return json.load(file)
    return {}

# Render avatar panel
def show_discern_avatar():
    profile = load_profile()

    st.markdown(f"### 🧠 {profile.get('name', 'DiscernAgent')} — *{profile.get('title', '')}*")
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=120)  # Iris avatar
    st.markdown(f"**Codename:** `{profile.get('code_name', '')}`")
    st.markdown(f"**Slogan:** *{profile.get('slogan', '')}*")
    st.markdown(f"**Personality:** {profile.get('persona', '')}")
    st.markdown(f"**Role:** {profile.get('role', '')}")
    st.markdown(f"**Version:** `{profile.get('version', '')}`")
    st.success(f"🟢 Status: {profile.get('status', 'unknown').capitalize()}")
