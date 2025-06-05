from core.notion_connector import get_notion_client

notion = get_notion_client()

response = notion.search(filter={"property": "object", "value": "database"})

print("\n🔍 Available Databases in your Notion workspace:\n")
for result in response["results"]:
    title = result["title"][0]["text"]["content"] if result["title"] else "Untitled"
    print(f"📘 {title}\n🆔 {result['id']}\n")
