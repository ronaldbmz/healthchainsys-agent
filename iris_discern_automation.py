from playwright.sync_api import sync_playwright
import time

def run_discern_query(saved_query_name="Physician Revenue Report"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        # Step 1: Go to Discern Analytics login page (update to your actual URL)
        page.goto("https://your-discern-url.com")  # ⛳️ Replace with actual Discern login link

        # Step 2: Wait for manual login
        print("🔐 Please log in manually if required...")
        page.wait_for_timeout(20000)  # Wait 20 seconds

        # Step 3: Navigate to Saved Queries
        print("📂 Navigating to Saved Queries...")
        page.click("text='Saved Queries'")  # 🔍 Adjust selector as needed

        # Step 4: Select the query to run
        print(f"🔍 Looking for saved query: {saved_query_name}")
        page.click(f"text='{saved_query_name}'")  # 🔍 Adjust based on your UI

        # Optional: Add date filter input here if required
        # page.fill("input[name='StartDate']", "06/01/2025")

        # Step 5: Export the file
        print("💾 Exporting the report...")
        page.click("text='Export'")  # Adjust this selector if needed

        # Step 6: Wait for the download to complete
        time.sleep(5)
        print("✅ Export complete. IRIS ready.")

        browser.close()
