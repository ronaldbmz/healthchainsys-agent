import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from notion_client import Client as NotionClient
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Notion and OpenAI
notion = NotionClient(auth=os.getenv("NOTION_TOKEN"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Block ID where MarketIntel insights are logged
NOTION_BLOCK_ID = os.getenv("NOTION_BLOCK_ID_MARKETINTEL_LOG")

# Function to scrape raw page text
def scrape_text(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text().strip()
    except Exception as e:
        return f"Error scraping {url}: {e}"

# Function to summarize using OpenAI
def summarize(text, source):
    prompt = f"""
You are a competitive market analyst for a healthcare data company.
From the following webpage content, extract the following:

1. Company name
2. Services offered
3. Pricing model (if mentioned)
4. Target market
5. Unique value proposition
6. Any strategic advantage or weakness
7. Opportunities HealthChainSys could exploit

Source: {source}

Content:
{text[:3000]}
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Push insight to Notion block
def push_to_notion_block(summary):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Split long text into chunks of 2000 characters or less
    paragraphs = []
    for i in range(0, len(summary), 2000):
        chunk = summary[i:i + 2000]
        paragraphs.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": chunk
                        }
                    }
                ]
            }
        })

    # Add a timestamp header
    notion.blocks.children.append(
        block_id=NOTION_BLOCK_ID,
        children=[
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": f"📌 Market Insight generated at {now}"
                            }
                        }
                    ]
                }
            },
            *paragraphs  # Add each chunk as a separate block
        ]
    )

# Run agent
def run_agent():
    sources = {
        "Sintra": "https://sintra.ai",
        "LeanAI": "https://leanaileaderboard.com"
    }

    for name, url in sources.items():
        print(f"Scraping {name}...")
        raw = scrape_text(url)
        if "Error" not in raw:
            print(f"Generating summary for {name}...")
            summary = summarize(raw, name)
            print("Pushing to Notion...")
            push_to_notion_block(summary)
            print(f"✅ {name} summary added.\n")
        else:
            print(raw)

# Script entry point
if __name__ == "__main__":
    run_agent()
