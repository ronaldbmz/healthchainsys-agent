import os
import json
from datetime import datetime, timedelta

REGISTRY_FILE = "data/insight_registry.json"
TIME_WINDOW_HOURS = 24

class InsightRegistry:
    def __init__(self):
        self._load_registry()

    def _load_registry(self):
        if os.path.exists(REGISTRY_FILE):
            with open(REGISTRY_FILE, "r") as f:
                self.entries = json.load(f)
        else:
            self.entries = []

    def _save_registry(self):
        with open(REGISTRY_FILE, "w") as f:
            json.dump(self.entries, f, indent=2)

    def is_duplicate(self, insight_text: str) -> bool:
        cutoff = datetime.now() - timedelta(hours=TIME_WINDOW_HOURS)
        self.entries = [
            entry for entry in self.entries
            if datetime.fromisoformat(entry["timestamp"]) > cutoff
        ]
        return any(entry["insight"] == insight_text for entry in self.entries)

    def add(self, insight_text: str):
        self.entries.append({
            "insight": insight_text,
            "timestamp": datetime.now().isoformat()
        })
        self._save_registry()
