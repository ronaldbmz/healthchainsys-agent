import os
from dotenv import load_dotenv
from core.discern_loader import load_discern_data

load_dotenv()

def get_structured_discern_data():
    data = load_discern_data()
    if not data:
        return []

    structured = []
    for row in data:
        structured.append({
            "procedure": row.get("Procedure", "").strip(),
            "date": row.get("Date", "").strip(),
            "surgeon": row.get("Surgeon", "").strip()
        })
    return structured

if __name__ == "__main__":
    for entry in get_structured_discern_data():
        print(entry)
        