import argparse
from core.discern_ingestor import run as run_discern_ingestor
from core.validation_agent import run_validation_agent
from core.validation_logger import push_validation_summary

def main():
    parser = argparse.ArgumentParser(description="HealthChainBot Desktop Agent")
    parser.add_argument("--pull-discern", action="store_true", help="Pull surgical case data from Discern")
    parser.add_argument("--validate", action="store_true", help="Run ValidationBot")
    parser.add_argument("--push", action="store_true", help="Manually push a validation summary")

    args = parser.parse_args()

    if args.pull_discern:
        print("🩺 Pulling data from Discern...")
        run_discern_ingestor()

    if args.validate:
        print("🧪 Running ValidationBot...")
        run_validation_agent()

    if args.push:
        print("📤 Manually pushing a test summary to Execution Planner...")
        push_validation_summary([], "manual_push.csv")

if __name__ == "__main__":
    main()
