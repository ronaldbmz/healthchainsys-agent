import os
from dotenv import load_dotenv
from datetime import datetime

from core.validator_engine import validate_file_against_schema
from core.validation_logger import push_validation_summary

# ✅ Load .env config
load_dotenv()

# 📁 Input File
CASE_FILE_PATH = "data/input/casetabs_schedule_sample.csv"

# 📐 Expected Schema
EXPECTED_SCHEMA = {
    "Case ID": str,
    "Surgeon": str,
    "Procedure": str,
    "Scheduled Start": str,
    "Room": str,
    "Status": str
}

# 🤖 Agent Logic
def run_casetabs_agent():
    print("\n📅 Starting CaseTabsAgent...\n")

    if not os.path.exists(CASE_FILE_PATH):
        print(f"❌ Input file not found at: {CASE_FILE_PATH}")
        return

    print(f"📄 Validating: {CASE_FILE_PATH}")
    validation_issues = validate_file_against_schema(CASE_FILE_PATH, EXPECTED_SCHEMA)

    if not validation_issues:
        print("✅ File passed all validation checks.\n")
    else:
        print("⚠️ Validation issues found:")
        for issue in validation_issues:
            print("  -", issue)

    # 🔁 Push to Notion Execution Planner
    push_validation_summary(validation_issues, CASE_FILE_PATH)

    print("✅ CaseTabsAgent completed.\n")


if __name__ == "__main__":
    run_casetabs_agent()
