from datetime import datetime
import random
import os
import sys
from notion_client import Client
from dotenv import load_dotenv

# 🔧 Ensure `utils` directory is added before importing
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.insight_registry import InsightRegistry

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_TOKEN")
NOTION_DB_ID_EXECUTION_LOG = os.getenv("NOTION_DB_ID_EXECUTION_LOG")
NOTION_USER_ID = os.getenv("NOTION_USER_ID")

notion = Client(auth=NOTION_API_KEY)
registry = InsightRegistry()

INSIGHT_TEMPLATES = [
    "📊 Validate healthtech BD accuracy through clinical trials.",
    "📈 Track patient acquisition growth across ASC vs HOPD site models.",
    "🧠 Monitor orthopedic volume market share by payor and subspecialty.",
    "💼 Launch targeted campaigns for orthopedic clinics based on regional outcome benchmarks."
]

def generate_market_insight():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    insight = random.choice(INSIGHT_TEMPLATES)
    summary = f"📈 Market Insight generated on {now} →\n{insight}"
    print("📈 Summary to push:", summary)

    # Check for duplicates
    if registry.is_duplicate(insight):
        print("⏩ Skipping duplicate Market Insight (already logged within 24 hours).")
        return

    try:
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
                    "select": {"name": "MarketIntel AI"}
                },
                "📊 Category": {
                    "multi_select": [{"name": "MarketIntel"}]
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
        print("✅ Market Insight pushed to Execution Tracker.")
    except Exception as e:
        print("❌ Failed to push Market Insight to Notion:", e)

    # Log the insight to registry
    registry.add(insight)

if __name__ == "__main__":
    generate_market_insight()


