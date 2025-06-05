
import os
from dotenv import load_dotenv
from notion_client import Client
from core.discern_loader import load_discern_data
from datetime import datetime

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DB_ID_EXECUTION_PLANNER = os.getenv("NOTION_DB_ID_EXECUTION_PLANNER")

notion = Client(auth=NOTION_TOKEN)

def format_summary(row):
    return f"💡 Surgical case: {row['Procedure']} scheduled for {row['Date']} by {row['Surgeon']}."

def push_insight_to_notion(summary):
    try:
        notion.pages.create(
            parent={"database_id": NOTION_DB_ID_EXECUTION_PLANNER},
            properties={
                "📌 Insight Summary": {
                    "title": [{"text": {"content": summary}}]
                },
                "📅 Date Logged": {
                    "date": {"start": datetime.now().isoformat()}
                },
                "📊 Source Agent": {
                    "select": {"name": "Surgical Strategist AI"}
                },
                "📁 Category": {
                    "multi_select": [{"name": "Surgical"}]
                },
                "⏳ Status": {
                    "select": {"name": "Pending"}
                },
                "👤 Owner": {
                    "rich_text": [{"text": {"content": "Ronald Manipol"}}]
                },
                "📝 Notes / Actions": {
                    "rich_text": []
                }
            }
        )
        print(f"✅ Insight pushed: {summary}")
    except Exception as e:
        print(f"❌ Failed to push insight: {summary}\n{e}")

def run():
    data = load_discern_data()
    for row in data:
        summary = format_summary(row)
        push_insight_to_notion(summary)

if __name__ == "__main__":
    run()
