from core.agents.discern.tasks import export_discern_data, validate_and_push

def run():
    print("🤖 Discern Agent is now active.")
    export_discern_data()
    validate_and_push()

if __name__ == "__main__":
    run()
