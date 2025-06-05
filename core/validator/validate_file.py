import pandas as pd
import os

# Set input and output paths
INPUT_PATH = "./data/input/march_cases_sample.csv"
OUTPUT_PATH = "./data/output/validated_march_cases.csv"

# Define required fields
REQUIRED_FIELDS = [
    "Patient ID", "Date of Surgery", "Surgeon Name",
    "Procedure Name", "CPT Code", "ASA Class",
    "BMI", "Discharge Disposition", "Diagnosis Code", "Laterality"
]

# Suggested CPT codes based on procedure names
CPT_SUGGESTIONS = {
    "Total Knee Arthroplasty": "27447",
    "Hip Replacement": "27130"
}

def validate_row(row):
    notes = []

    # Check required fields
    for field in REQUIRED_FIELDS:
        if pd.isna(row[field]) or str(row[field]).strip() == "":
            notes.append(f"Missing: {field}")

    # Autofill suggestion for CPT Code
    if (not row.get("CPT Code") or str(row["CPT Code"]).strip() == ""):
        suggestion = CPT_SUGGESTIONS.get(row["Procedure Name"], None)
        if suggestion:
            notes.append(f"Suggested CPT: {suggestion}")

    return "; ".join(notes)

def validate_file(file_path):
    df = pd.read_csv(file_path)

    def validate_row(row):
        notes = []
        for field in REQUIRED_FIELDS:
            if pd.isna(row[field]) or str(row[field]).strip() == "":
                notes.append(f"Missing: {field}")
        if (not row.get("CPT Code") or str(row["CPT Code"]).strip() == ""):
            suggestion = CPT_SUGGESTIONS.get(row["Procedure Name"], None)
            if suggestion:
                notes.append(f"Suggested CPT: {suggestion}")
        return "; ".join(notes)

    df["Validation Notes"] = df.apply(validate_row, axis=1)

    # Save the output file
    output_path = "./data/output/validated_output.csv"
    df.to_csv(output_path, index=False)

    flagged_rows = df[df["Validation Notes"] != ""]
    return f"{len(df)} cases processed.\n{len(flagged_rows)} rows flagged.\nOutput saved to: {output_path}"
