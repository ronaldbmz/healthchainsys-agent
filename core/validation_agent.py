import os
from dotenv import load_dotenv
from datetime import datetime

# ✅ Core functions
from core.validator_engine import validate_file_against_schema
from core.validation_logger import push_validation_summary

# 📦 Load environment variables
load_dotenv()

# 📄 Target file path
SAMPLE_FILE_PATH = "data/input/march_cases_sample.csv"

# 🧪 Define expected schema
EXPECTED_SCHEMA = {
    "Patient ID": str,
    "Surgeon": str,
    "Procedure": str,
    "ScheduledStartTime": str,
    "ActualStartTime": str
}

def run_validation_agent():
    print("\n🔍 Starting ValidationBot agent...\n")

    if not os.path.exists(SAMPLE_FILE_PATH):
        print(f"❌ Input file not found at: {SAMPLE_FILE_PATH}")
        return

    print(f"📄 Validating: {SAMPLE_FILE_PATH}")
    validation_issues = validate_file_against_schema(SAMPLE_FILE_PATH, EXPECTED_SCHEMA)

    if not validation_issues:
        print("✅ File passed all validation checks.\n")
    else:
        print("⚠️ Validation issues found:")
        for issue in validation_issues:
            print("  -", issue)

    push_validation_summary(validation_issues, SAMPLE_FILE_PATH)

if __name__ == "__main__":
    run_validation_agent()

