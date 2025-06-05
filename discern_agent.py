import os
from datetime import datetime
from core.agents.discern.scripts.controller import launch_discern_browser
from core.discern_ingestor import run as run_discern_ingestor
from core.validation_agent import run_validation_agent
from core.validation_logger import push_validation_summary

def run_full_discern_agent(saved_query=None):
    print("🧠 Launching DiscernAgent...")

    # Step 1: Launch Discern and export query
    launch_discern_browser(saved_query=saved_query)

    # Step 2: Rename the exported rptdocument.csv file
    export_folder = "data/raw_discern_exports"
    filename = "rptdocument.csv"
    full_path = os.path.join(export_folder, filename)

    if not os.path.exists(full_path):
        print("❌ No exported rptdocument.csv file found.")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = saved_query if saved_query else "discern_export"
    new_name = f"{base_name}_{timestamp}.csv"
    new_path = os.path.join(export_folder, new_name)

    os.rename(full_path, new_path)
    print(f"📁 Renamed file to: {new_path}")

    # Step 3: Ingest → Validate → Push summary
    run_discern_ingestor()
    run_validation_agent()
    push_validation_summary([], new_name)

    print("✅ DiscernAgent full cycle completed.")

if __name__ == "__main__":
    run_full_discern_agent()
