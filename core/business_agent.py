from datetime import datetime
from notion_client import Client
from dotenv import load_dotenv
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.insight_registry import InsightRegistry

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_TOKEN")
NOTION_DB_ID_EXECUTION_LOG = os.getenv("NOTION_DB_ID_EXECUTION_LOG")
NOTION_USER_ID = os.getenv("NOTION_USER_ID")

notion = Client(auth=NOTION_API_KEY)
registry = InsightRegistry()

def generate_business_insight():
    try:
        insight = "📈 Improve payer mix through direct-to-employer and bundled contract models."
        print(f"💼 Summary to push: {insight}")

        if registry.is_duplicate(insight):
            print("⚠️ Skipping duplicate insight (already logged within 24 hours).")
            return

        notion.pages.create(
            parent={"database_id": NOTION_DB_ID_EXECUTION_LOG},
            properties={
                "📌 Insight Summary": {
                    "title": [{"text": {"content": insight}}]
                },
                "📅 Date Logged": {
                    "date": {"start": datetime.now().isoformat()}
                },
                "🧠 Source Agent": {
                    "select": {"name": "Business Strategist AI"}
                },
                "📊 Category": {
                    "multi_select": [{"name": "Business"}]
                },
                "✅ Status": {
                    "select": {"name": "Pending"}
                },
                "👤 Owner": {
                    "people": [{"object": "user", "id": NOTION_USER_ID}]
                },
                "📝 Notes / Actions": {
                    "rich_text": []
                }
            }
        )

        print("✅ Business Insight pushed to Execution Tracker.")
        registry.add(insight)

    except Exception as e:
        print("❌ Failed to push Business Insight to Notion:", e)

if __name__ == "__main__":
    generate_business_insight()
