from notion_client import Client
import os
from dotenv import load_dotenv

load_dotenv()

notion = Client(auth=os.getenv("NOTION_TOKEN"))
users = notion.users.list()

for user in users['results']:
    print(f"Name: {user['name']}")
    print(f"ID: {user['id']}")
    print(f"Type: {user['type']}")
    print("-" * 40)
