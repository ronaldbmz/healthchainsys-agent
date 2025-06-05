import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
from discern_agent import run_full_discern_agent

# Folder to watch for exports
WATCH_FOLDER = "data/raw_discern_exports"
FILENAME = "rptdocument.csv"

# Set your saved_query key manually for now
SAVED_QUERY = "surgical_cases"  # Later, we will make this dynamic

class DiscernExportHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and FILENAME in event.src_path:
            print(f"📁 Detected export: {event.src_path}")
            time.sleep(2)  # Allow file to fully write

            # Rename with timestamp and saved_query
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_name = f"{SAVED_QUERY}_{timestamp}.csv"
            new_path = os.path.join(WATCH_FOLDER, new_name)
            os.rename(event.src_path, new_path)

            print(f"✅ Renamed to: {new_path}")
            run_full_discern_agent(saved_query=SAVED_QUERY)  # Trigger with label

def start_watcher():
    observer = Observer()
    event_handler = DiscernExportHandler()
    observer.schedule(event_handler, path=WATCH_FOLDER, recursive=False)
    observer.start()
    print(f"👀 Watching for {FILENAME} in: {WATCH_FOLDER}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_watcher()
