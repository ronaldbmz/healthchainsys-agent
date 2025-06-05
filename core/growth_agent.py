import os
import sys
import random
from datetime import datetime
from notion_client import Client
from dotenv import load_dotenv

# Ensure utils is accessible when run as a script
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.insight_registry import InsightRegistry

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_TOKEN")
NOTION_BLOCK_ID_GROWTH_LOG = os.getenv("NOTION_BLOCK_ID_GROWTH_LOG")
NOTION_DB_ID_EXECUTION_LOG = os.getenv("NOTION_DB_ID_EXECUTION_LOG")
BOT_USER_ID = os.getenv("BOT_USER_ID")

notion = Client(auth=NOTION_API_KEY)
registry = InsightRegistry()

INSIGHT_TEMPLATES = [
    "📦 Package HealthChainBot’s validation + dashboard services for orthopedic clinics.",
    "💰 Introduce tiered pricing models for HealthChainBot services based on data volume.",
    "📊 Build a monetization plan around AAOS RegistrySync integration.",
    "🏥 Target ambulatory surgical centers with a bundled AI performance suite.",
    "📈 Offer payers predictive dashboard services via annual subscriptions.",
    "🤝 Partner with healthtech distributors to resell all analytics modules.",
    "🧠 Monetize benchmarking data across markets with anonymized reporting."
]

def generate_growth_insight():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    insight = random.choice(INSIGHT_TEMPLATES)
    summary = f"📌 Growth Insight generated on {now} →\n{insight}"
    print("📌 Summary to push:", summary)

    # Check for duplicates
    if registry.is_duplicate(insight):
        print("⚠️ Skipping duplicate insight (already logged within 24 hours).")
        return

    # Push to Growth Strategy Notion page
    try:
        notion.blocks.children.append(
            NOTION_BLOCK_ID_GROWTH_LOG,
            children=[
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {"type": "text", "text": {"content": summary[:2000]}}
                        ]
                    }
                }
            ]
        )
        print("✅ Insight pushed to Growth Strategy page.")
    except Exception as e:
        print("❌ Failed to push to Notion (Growth page):", e)

    # Push to Execution Tracker Table
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
        "select": {"name": "GrowthAdvisor AI"}
    },
    "📊 Category": {
        "multi_select": [{"name": "Growth"}]
    },
    "✅ Status": {
        "select": {"name": "Pending"}
    },
    "📝 Notes / Actions": {
        "rich_text": []
    }
}
        )
        print("✅ Insight also pushed to Execution Tracker table.")
    except Exception as e:
        print("❌ Failed to push to Execution Tracker:", e)

    # Log the insight in the registry
    registry.add(insight)

if __name__ == "__main__":
    generate_growth_insight()


