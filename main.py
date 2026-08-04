import sys
import os

# Fix module import paths dynamically for any environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.key_manager import SarvKeyManager
from api.sarv_router import SarvAPIRouter
from modules.automation import SystemAutomation
from config.settings import APP_NAME, VERSION

def main():
    print(f"=== {APP_NAME} v{VERSION} ===")
    
    key_mgr = SarvKeyManager()
    router = SarvAPIRouter()
    auto = SystemAutomation()

    # Generate or reuse API key on startup
    print("\n--- Initializing SARV API Key System ---")
    key_data = key_mgr.generate_api_key(client_name="JARVIS-Desktop", key_type="live")
    active_key = key_data["api_key"]

    print(f"🔑 Active Key : {active_key}")
    print("🔒 SHA-256 Hash stored in config/api_keys.json\n")

    while True:
        cmd = input("SARV OS > ").strip()
        if cmd.lower() in ["exit", "quit"]:
            print("Shutting down SARV OS...")
            break
        elif not cmd:
            continue
        elif cmd.lower().startswith("create "):
            parts = cmd.split(" ", 2)
            if len(parts) == 3:
                res = auto.create_text_file(parts[1], parts[2])
                print(res)
            else:
                print("Usage: create <filename> <content>")
        else:
            response = router.process_request(api_key=active_key, command=cmd)
            print(f"Response: {response}\n")

if __name__ == "__main__":
    main()