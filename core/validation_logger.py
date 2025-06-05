import os
from datetime import datetime
from notion_client import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DB_ID_EXECUTION_PLANNER = os.getenv("NOTION_DB_ID_EXECUTION_PLANNER")
notion = Client(auth=NOTION_TOKEN)

def push_validation_summary(validation_issues, file_path):
    status = "Issues Found" if validation_issues else "Complete"
    notes = "\n".join(validation_issues) if validation_issues else "No validation issues found."
    
    try:
        response = notion.pages.create(
            parent={"database_id": NOTION_DB_ID_EXECUTION_PLANNER},
            properties={
                "📌 Insight Summary": {
                    "title": [{
                        "text": {
                            "content": f"🧪 Validation run on {file_path} @ {datetime.now().isoformat()}"
                        }
                    }]
                },
                "📅 Date Logged": {
                    "date": {"start": datetime.now().isoformat()}
                },
                "🧠 Source Agent": {
                    "select": {"name": "ValidationBot"}
                },
                "🧭 Category": {
                    "multi_select": [{"name": "Validation"}]
                },
                "📎 Notes / Actions": {
                    "rich_text": [{"text": {"content": notes}}]
                },
                "⏳ Status": {
                    "select": {"name": status}
                },
                "👤 Owner": {
                    "rich_text": [{"text": {"content": "Ronald Manipol"}}]
                }
            }
        )
        print("✅ Validation summary pushed to Execution Planner.")
    except Exception as e:
        print("❌ Failed to push validation summary:", e)
