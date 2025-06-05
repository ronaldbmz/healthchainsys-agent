import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_TOKEN")
NOTION_USER_ID = os.getenv("NOTION_USER_ID")
notion = Client(auth=NOTION_API_KEY)

def comment_on_page(page_id, comment_text):
    try:
        notion.comments.create(
            parent={"page_id": page_id},
            rich_text=[{"type": "text", "text": {"content": comment_text}}],
        )
        print(f"💬 Comment posted on page {page_id}")
    except Exception as e:
        print(f"❌ Failed to post comment: {e}")
