import os
import time
import webbrowser
from datetime import datetime
from dotenv import load_dotenv
from core.discern_ingestor import run as run_discern_ingestor
from core.validation_agent import run_validation_agent
from core.validation_logger import push_validation_summary

# Load environment variables
load_dotenv()

def launch_discern_browser(saved_query="Physician Revenue Report"):
    print("🧠 IRIS Notice: Cerner Discern launches through Citrix.")
    print("👉 Launching login URL in your default browser...")
    print("   https://cerncomo-ext.cernerworks.com")
    print("🔐 Complete Duo MFA, launch Discern Analytics, and export your report.")
    print("📥 IRIS will wait for 'rptdocument.csv' in your Downloads or export folder.")

    # Open login URL
    webbrowser.open("https://cerncomo-ext.cernerworks.com")

def run_full_discern_agent(saved_query=None):
    print("🧠 Launching IRIS DiscernAgent in assisted manual mode...")

    # Step 1: Show instructions + open login link
    launch_discern_browser(saved_query)

    # Step 2: Wait for rptdocument.csv to appear
    export_folder = os.getenv("DISCERN_FILE_PATH", "/Users/Bianca/Downloads")
    filename = "rptdocument.csv"
    full_path = os.path.join(export_folder, filename)

    print(f"🔍 Watching for file: {full_path}")
    timeout = 600  # Wait up to 10 minutes
    start_time = time.time()

    while not os.path.exists(full_path):
        if time.time() - start_time > timeout:
            print("❌ Timeout: rptdocument.csv not detected in time.")
            return
        time.sleep(5)

    print(f"📁 File detected: {full_path}")

    # Step 3: Rename the file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = saved_query if saved_query else "discern_export"
    new_name = f"{base_name}_{timestamp}.csv"
    new_path = os.path.join(export_folder, new_name)

    os.rename(full_path, new_path)
    print(f"📄 Renamed file to: {new_path}")

    # Step 4: Ingest → Validate → Push summary
    run_discern_ingestor(new_path)
    run_validation_agent()
    push_validation_summary([], new_name)

    print("✅ DiscernAgent full cycle completed.")

if __name__ == "__main__":
    run_full_discern_agent()
