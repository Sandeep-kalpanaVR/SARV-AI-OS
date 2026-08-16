from modules.intent_engine import SarvIntentParser
from modules.system_executor import SarvSystemExecutor

# Initialize Core Modules
parser = SarvIntentParser()
executor = SarvSystemExecutor()

# 1. Parse Command
user_command = "SARV, launch VS Code and check cloud router status"
print(f"📥 Input Command: {user_command}\n")

parsed_json = parser.parse_command(user_command)
print("🤖 Parsed Intent JSON:")
print(parsed_json)

# 2. Execute Actions Locally
print("\n⚡ Executing OS Actions...")
execution_results = executor.execute_actions(parsed_json["actions"])

for result in execution_results:
    print(f"  └─ Step {result['step']} [{result['target']}]: {result['status']}")