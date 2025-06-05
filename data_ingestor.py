import os
import time
import glob
from datetime import datetime
import subprocess

WATCH_FOLDER = "/Users/Bianca/Downloads/Discern"
PROCESSED_FOLDER = os.path.join(WATCH_FOLDER, "processed")

if not os.path.exists(PROCESSED_FOLDER):
    os.makedirs(PROCESSED_FOLDER)

def run_validation(file_path):
    print(f"🔍 Detected new file: {file_path}")
    try:
        subprocess.run([
            "python",
            "core/surgical_validator.py",
            file_path
        ], check=True)
        print("✅ Validation triggered.")
    except subprocess.CalledProcessError as e:
        print("❌ Error running validation:", e)

def monitor_folder():
    print("👀 Monitoring for new CSVs in:", WATCH_FOLDER)
    seen = set()

    while True:
        files = glob.glob(os.path.join(WATCH_FOLDER, "cases_*.csv"))
        for file_path in files:
            filename = os.path.basename(file_path)
            if filename not in seen:
                seen.add(filename)
                run_validation(file_path)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                new_path = os.path.join(PROCESSED_FOLDER, f"{filename}.{timestamp}.bak")
                os.rename(file_path, new_path)
                print(f"📦 Moved to: {new_path}")
        time.sleep(5)

if __name__ == "__main__":
    monitor_folder()
