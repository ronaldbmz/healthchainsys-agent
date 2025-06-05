import csv
import os
from dotenv import load_dotenv

# Load environment variables (if needed for later Notion logging or file paths)
load_dotenv()

# Define expected schema (can later be loaded dynamically)
EXPECTED_SCHEMA = [
    "PatientID",
    "ProcedureDate",
    "Surgeon",
    "ProcedureName",
    "ScheduledStartTime",
    "ActualStartTime",
    "ORRoom",
    "CaseStatus"
]
import os
print(f"🧭 Current working directory: {os.getcwd()}")

# Path to test file (update to your local CSV location)
SAMPLE_FILE_PATH = "data/input/sample_or_schedule.csv"

def validate_file_against_schema(file_path, expected_schema):
    errors = []
    try:
        with open(file_path, mode="r", newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            actual_fields = reader.fieldnames

            # Check for missing fields
            missing = [field for field in expected_schema if field not in actual_fields]
            if missing:
                errors.append(f"❌ Missing fields: {missing}")

            # Check for unexpected fields
            extra = [field for field in actual_fields if field not in expected_schema]
            if extra:
                errors.append(f"⚠️ Unexpected fields: {extra}")

            # Optionally: check first 3 rows for nulls
            row_count = 0
            for row in reader:
                row_count += 1
                for field in expected_schema:
                    if field in row and row[field] == "":
                        errors.append(f"Empty value found in row {row_count}, column '{field}'")
                if row_count >= 3:
                    break

    except Exception as e:
        errors.append(f"Error reading file: {e}")

    return errors

if __name__ == "__main__":
    print("🧪 Running ValidationBot (validator_engine.py)...")

    if not os.path.exists(SAMPLE_FILE_PATH):
        print(f"❌ Sample file not found at: {SAMPLE_FILE_PATH}")
    else:
        validation_issues = validate_file_against_schema(SAMPLE_FILE_PATH, EXPECTED_SCHEMA)

        if not validation_issues:
            print("✅ File passed all schema checks.")
        else:
            print("⚠️ Validation issues found:")
            for issue in validation_issues:
                print(" -", issue)

