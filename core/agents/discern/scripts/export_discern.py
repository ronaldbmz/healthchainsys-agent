from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

def launch_discern_browser():
    print("🚀 Launching Chrome browser for Discern export...")

    # Initialize ChromeDriver (make sure it's in your PATH)
    service = Service()  # Uses default install path
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)

    # Go to Discern login
    driver.get("https://uhg.cmwhospitals.com/DiscernAnalytics2")

    print("🔐 Please complete login manually (for now)...")
    time.sleep(30)  # Give user time to login

    # You’ll automate further in next steps...
    driver.quit()
