# execution_bot.py
import os
from datetime import datetime, timedelta
from notion_client import Client
from dotenv import load_dotenv
from dateutil import parser

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DB_ID_EXECUTION_LOG = os.getenv("NOTION_DB_ID_EXECUTION_LOG")
NOTION_USER_ID = os.getenv("NOTION_USER_ID")  # Our verified user ID for ownership assignment

notion = Client(auth=NOTION_TOKEN)

def get_pending_insights():
    print("🔍 Fetching insights with 'Pending' status...")
    try:
        response = notion.databases.query(
            database_id=NOTION_DB_ID_EXECUTION_LOG,
            filter={
                "property": "✅ Status",
                "select": {"equals": "Pending"}
            }
        )
        return response["results"]
    except Exception as e:
        print("❌ Error while querying database:", e)
        return []

def update_status_to_in_progress(page_id):
    notion.pages.update(
        page_id=page_id,
        properties={
            "✅ Status": {"select": {"name": "In Progress"}}
        }
    )
    print(f"🚀 Updated status to 'In Progress' for {page_id}")

def assign_owner(page_id):
    notion.pages.update(
        page_id=page_id,
        properties={
            "👤 Owner": {"people": [{"object": "user", "id": NOTION_USER_ID}]}
        }
    )
    print(f"👤 Owner assigned to {NOTION_USER_ID} for {page_id}")

def flag_if_old(page_id, logged_date):
    dt_logged = parser.isoparse(logged_date)
    if datetime.now(dt_logged.tzinfo) - dt_logged > timedelta(hours=48):
        notes = "⚠️ Insight still pending >48 hours. Needs review."
        notion.pages.update(
            page_id=page_id,
            properties={
                "📝 Notes / Actions": {
                    "rich_text": [{"type": "text", "text": {"content": notes}}]
                }
            }
        )
        print(f"🚩 Flagged old insight: {page_id}")

def run_bot():
    insights = get_pending_insights()
    print(f"📦 Found {len(insights)} pending insights.")
    for page in insights:
        try:
            page_id = page["id"]
            properties = page["properties"]
            owner = properties.get("👤 Owner", {}).get("people", [])
            date_logged = properties["📅 Date Logged"]["date"]["start"]

            if not owner:
                assign_owner(page_id)

            flag_if_old(page_id, date_logged)
            update_status_to_in_progress(page_id)

        except Exception as e:
            print(f"❌ Error processing page {page['id']}: {e}")

if __name__ == "__main__":
    run_bot()
