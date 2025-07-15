import streamlit as st
from discern_agent import run_full_discern_agent
from core.validation_agent import run_validation_agent
from core.validation_logger import push_validation_summary

st.set_page_config(page_title="HealthChainSys Agent Dashboard", layout="centered")

st.title("🤖 HealthChainSys Agent Dashboard")
st.markdown("---")

# 🎭 IRIS Avatar
st.image("assets/iris_avatar.gif", caption="IRIS: Discern Intelligence Agent", width=140)

# 🧠 Discern Agent (IRIS)
st.header("🧠 Discern Agent (IRIS)")

# 🔁 Saved queries mapped from DA2 Book → actual Discern saved queries
saved_queries = {
    "Physician Revenue Report": "Physician Revenue",
    "Case Volume by Surgeon": "ZH OR Log EMCTCTX",
    "Patient Demographics Summary": "Patient Detail",
    "Procedure Cost and Supply": "ZH Supply Chain - Surgery Item Usage EMCTCTX",
    "Inventory Utilization": "ZH Supply Chain - Surgery Item Usage EMCTCTX",
    "Vendor Spend Analysis": "VendorDetails",
    "Revenue Details by Patient": "Revenue Details with patient",
    "Supply Chain Master": "Supply Chain - Primary Item Master 4.0 EMCTCTX",
    "OR Log": "ZH OR Log EMCTCTX",
    "Surgery - Implant Log": "Surgery - Implant Log 2 EMCTCTX",
    "Encounter Charges": "Report Designer Encounter Query"
}

query_name = st.selectbox("📂 Select a saved query to run:", list(saved_queries.keys()))
selected_query_id = saved_queries[query_name]

# 🚦 Execution Control
st.subheader("🧰 Execution Mode")
run_mode = st.selectbox("⚙️ Execution Mode:", ["Run Only IRIS", "Run All Agents (IRIS → Validation → Notion)"])

if st.button("▶️ Run Selected Workflow!"):
    with st.spinner("Running agents. Please wait..."):
        run_full_discern_agent(saved_query=selected_query_id)

        if run_mode == "Run All Agents (IRIS → Validation → Notion)":
            run_validation_agent()
            push_validation_summary([], selected_query_id)

st.markdown("---")

# 📊 TableauBot Placeholder
st.header("📊 TableauBot [Coming Soon]")
st.write("TableauBot will push validated data to Tableau dashboards automatically.")

# 🔎 Notion Integration Preview
st.header("📁 Notion Dashboard Preview")
st.write("Live view of Execution Planner in Notion (read-only):")

notion_url = "https://www.notion.so/1f28cb3532fc0868c9702eef8f5f71v1f28cb3532fc0868c9702eef8f5f1df5"
st.components.v1.iframe(notion_url, height=500, scrolling=True)

st.markdown("---")
st.success("✅ Agent Dashboard Ready 🧠")
