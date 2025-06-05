import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_TOKEN")
notion = Client(auth=NOTION_API_KEY)

def get_notion_client():
    return notion
