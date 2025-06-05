import streamlit as st
from discern_agent import run_full_discern_agent

st.set_page_config(page_title="HealthChainSys Agent Dashboard", layout="centered")

st.title("🤖 HealthChainSys Agent Dashboard")
st.markdown("---")

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

if st.button("▶️ Run Discern Agent for selected query"):
    with st.spinner("IRIS is working..."):
        run_full_discern_agent(saved_query=selected_query_id)

st.markdown("---")

# 📊 Add other agents below this section when ready (e.g., TableauBot, CaseTabsAgent, etc.)
st.info("More AI modules coming soon — including Tableau push and CaseTabs automation.")
