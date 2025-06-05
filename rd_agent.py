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

notion = Client(auth=NOTION_API_KEY)
registry = InsightRegistry()

INSIGHT_TEXT = "🧠 Partner with academic R&D centers to co-develop precision outcome models."

def generate_rd_insight():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    summary = f"📌 R&D Insight generated on {now} →\n{INSIGHT_TEXT}"
    print("📌 Summary to push:", summary)

    # Skip if duplicate
    if registry.is_duplicate(INSIGHT_TEXT):
        print("⚠️ Skipping duplicate insight (already logged within 24 hours).")
        return

    try:
        notion.pages.create(
            parent={"database_id": NOTION_DB_ID_EXECUTION_LOG},
            properties={
                "📌 Insight Summary": {
                    "title": [{"text": {"content": INSIGHT_TEXT}}]
                },
                "📅 Date Logged": {
                    "date": {"start": datetime.now().isoformat()}
                },
                "🧠 Source Agent": {
                    "select": {"name": "R&D Strategist AI"}
                },
                "📊 Category": {
                    "multi_select": [{"name": "R&D"}]
                },
                "✅ Status": {
                    "select": {"name": "Pending"}
                },
                "📝 Notes / Actions": {
                    "rich_text": []
                }
            }
        )
        print("✅ Insight pushed to Execution Tracker.")
    except Exception as e:
        print("❌ Failed to push insight to Notion:", e)

    # Log locally to prevent future duplication
    registry.add(INSIGHT_TEXT)

if __name__ == "__main__":
    generate_rd_insight()




