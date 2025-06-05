from datetime import datetime
from notion_client import Client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DB_ID_EXECUTION_PLANNER = os.getenv("NOTION_DB_ID_EXECUTION_PLANNER")

notion = Client(auth=NOTION_TOKEN)

def push_to_execution_planner():
    try:
        # Generate unique summary using timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        summary = f"🚀 Sample push from pusher.py @ {timestamp}"

        notion.pages.create(
            parent={"database_id": NOTION_DB_ID_EXECUTION_PLANNER},
            properties={
                "📌 Insight Summary": {
                    "title": [
                        {
                            "text": {
                                "content": summary
                            }
                        }
                    ]
                },
                "📅 Date Logged": {
                    "date": {
                        "start": datetime.now().isoformat()
                    }
                },
                "🧠 Source Agent": {
                    "select": {
                        "name": "Surgical Strategist AI"
                    }
                },
                "🧭 Category": {
                    "multi_select": [
                        {"name": "Surgical"}
                    ]
                },
                "👤 Owner": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "Ronald Manipol"
                            }
                        }
                    ]
                },
                "📎 Notes / Actions": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "Pushed sample record successfully to match all fields."
                            }
                        }
                    ]
                },
                "⏳ Status": {
                    "select": {
                        "name": "Pending"
                    }
                }
            }
        )

        print("✅ Insight pushed to Execution Planner.")

    except Exception as e:
        print("❌ Failed to push insight to Execution Planner:", e)

if __name__ == "__main__":
    push_to_execution_planner()
