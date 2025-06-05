import os
import pandas as pd
from datetime import datetime

def load_discern_data(file_path="data/raw_discern_exports/revenue_details_june_2025.csv"
):
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return []

    try:
        df = pd.read_csv(file_path)

        # Normalize column names
        df.columns = [col.strip().replace(' ', '_').lower() for col in df.columns]

        # Rename columns to match expected keys
        column_mapping = {
            'procedure': 'Procedure',
            'date': 'Date',
            'surgeon': 'Surgeon',
            'cpt_code': 'CPT_Code',
            'or_room': 'OR_Room',
            'status': 'Status',
            'actual_start': 'Actual_Start',
            'scheduled_start': 'Scheduled_Start'
        }
        df = df.rename(columns=column_mapping)

        # Convert date fields to datetime objects
        for date_col in ['Date', 'Actual_Start', 'Scheduled_Start']:
            if date_col in df.columns:
                df[date_col] = pd.to_datetime(df[date_col], errors='coerce')

        # Drop rows with missing essential information
        df = df.dropna(subset=['Procedure', 'Date', 'Surgeon'])

        # Convert DataFrame to list of dictionaries
        data = df.to_dict(orient='records')
        return data

    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return []
