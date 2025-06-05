from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

def launch_discern_browser(saved_query=None):
    print("🧠 Launching Discern Analytics via Chrome...")

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.headless = False

    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    # Chrome binary + Chromedriver path
    chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    driver_path = "/usr/local/bin/chromedriver"
    service = Service(executable_path=driver_path)

    # Launch browser
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Go to Discern login
    driver.get("https://cerncomo-ext.cernerworks.com")
    print("🔐 Discern loaded. Please complete MFA login manually...")
    time.sleep(60)

    # Search and open saved query if provided
    if saved_query:
        try:
            print(f"🔍 Searching for saved query: {saved_query}")
            search_box = driver.find_element("id", "navSearchBox")  # ← Confirm this ID matches Discern search
            search_box.clear()
            search_box.send_keys(saved_query)
            time.sleep(2)
            search_box.send_keys(Keys.ENTER)
            print("📄 Saved query entered. Waiting for page to load...")
            time.sleep(15)
        except Exception as e:
            print(f"⚠️ Failed to interact with saved query search: {e}")

    # Pause until user finishes export
    input("🖱️ Press ENTER after login + export is complete...")

    # Close browser
    driver.quit()
    print("✅ DiscernAgent session complete. Closing browser.")
