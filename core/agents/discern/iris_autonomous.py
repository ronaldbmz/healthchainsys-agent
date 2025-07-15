import os
from datetime import datetime
from core.discern_ingestor import run as run_discern_ingestor
from core.validation_agent import run_validation_agent
from core.validation_logger import push_validation_summary

# 📌 IRIS Master Report Map
iris_report_map = {
    "IRIS_patient encounter claim": {
        "label": "encounter_claim",
        "domain": "CWC Encounter"
    },
    "IRIS_person_ID_MRN_FIN": {
        "label": "id_mrn_fin",
        "domain": "CWC Person"
    },
    "IRIS_Surgery - Implant Log": {
        "label": "surgery_implant_log",
        "domain": "CWC Person"
    },
    "IRIS_Surgery - OR Log": {
        "label": "surgery_or_log",
        "domain": "CWC Person"
    },
    "IRIS_PO_per_patient": {
        "label": "po_per_patient",
        "domain": "CWC Supply Chain Purchase Order"
    },
    "IRIS_Patient Accounting - Revenue By Service Date": {
        "label": "revenue_by_date",
        "domain": "CWF GS Revenue"
    },
    "IRIS_Patient Accounting - Payments Extract": {
        "label": "payments_extract",
        "domain": "CWF GS Payments"
    }
}

def launch_discern_browser():
    cerner_url = "https://cerncomo-ext.cernerworks.com"
    print("🔐 Launching Safari and opening Cerner login portal...")
    os.system(f"open -a Safari '{cerner_url}'")
    print("🔐 Please log in manually (DUO) and open Discern via Citrix...")


def run_full_iris_autonomous():
    print("🧠 Launching IRIS Autonomous (Safari Mode)...")

    # Step 1: Manual login
    launch_discern_browser()
    input("🕐 Once fully logged in and Discern is open, press Enter to continue...")

    # Step 2: For each report, prompt user to export, then rename
    export_folder = "data/raw_discern_exports"
    timestamp_group = datetime.now().strftime("%Y%m%d_%H%M%S")

    renamed_files = []

    for report_name, meta in iris_report_map.items():
        print(f"\n📄 Now export: {report_name}")
        input("💾 After exporting, press Enter to continue...")

        raw_file = os.path.join(export_folder, "rptdocument.csv")
        if not os.path.exists(raw_file):
            print(f"❌ rptdocument.csv not found for {report_name}. Skipping.")
            continue

        new_filename = f"{meta['label']}_{timestamp_group}.csv"
        new_path = os.path.join(export_folder, new_filename)

        os.rename(raw_file, new_path)
        print(f"✅ Renamed: {new_filename}")
        renamed_files.append(new_filename)

    # Step 3: Ingest → Validate → Push summary
    print("\n🔍 Processing all exported reports...")
    run_discern_ingestor()
    run_validation_agent()

    for file in renamed_files:
        push_validation_summary([], file)

    print("✅ IRIS Autonomous run completed.")

if __name__ == "__main__":
    run_full_iris_autonomous()
