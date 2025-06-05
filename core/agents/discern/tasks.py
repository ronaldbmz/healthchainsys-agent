from core.discern_loader import load_discern_data
from core.validation_agent import run_validation_agent
from core.validation_logger import push_validation_summary

def export_discern_data():
    print("📤 Simulating Discern data export... (to be automated)")
    # Future: use scripts/export_discern.py
    return

def validate_and_push():
    print("✅ Validating exported data...")
    run_validation_agent()
