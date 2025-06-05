import os
from datetime import datetime
from notion_client import Client
from dotenv import load_dotenv
from dateutil import parser

# Load environment variables
load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
EXECUTION_DB_ID = os.getenv("NOTION_DB_ID_EXECUTION_LOG")
DEFAULT_OWNER_ID = os.getenv("NOTION_USER_ID")  # Valid for assigning Person fields

notion = Client(auth=NOTION_TOKEN)

def get_pending_insights():
    response = notion.databases.query(
        **{
            "database_id": EXECUTION_DB_ID,
            "filter": {
                "and": [
                    {
                        "property": "✅ Status",
                        "select": {
                            "equals": "Pending"
                        }
                    },
                    {
                        "property": "📅 Date Logged",
                        "date": {
                            "on_or_before": datetime.now().isoformat()
                        }
                    }
                ]
            }
        }
    )
    return response["results"]

def log_execution_task(insight_source, summary):
    response = notion.pages.create(
        parent={"database_id": EXECUTION_DB_ID},
        properties={
            "📌 Insight Summary": {
                "title": [{
                    "type": "text",
                    "text": {
                        "content": summary[:200]  # Limit to 200 chars to avoid Notion error
                    }
                }]
            },
            "✅ Status": {
                "select": {
                    "name": "Pending"
                }
            },
            "📅 Date Logged": {
                "date": {
                    "start": datetime.now().isoformat()
                }
            },
            "👤 Owner": {
                "people": [{
                    "id": DEFAULT_OWNER_ID
                }]
            }
        }
    )

    print(f"✅ Execution task from {insight_source} logged.")

# Test it
if __name__ == "__main__":
    log_execution_task("MarketIntel", "Generated summary for Sintra.ai and LeanAI")
