import os
import sys
import json
import requests

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from modules.system_executor import SarvSystemExecutor
from modules.messaging_bridge import SarvMessagingBridge
from modules.computer_control import SarvComputerControl
from modules.anti_theft import SarvAntiTheft
from modules.intent_engine import SarvIntentParser
from modules.voice_engine import SarvVoiceEngine

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config", "agent_config.json")

class SarvDesktopAgent:
    def __init__(self, gateway_url: str):
        self.gateway_url = gateway_url.rstrip("/")
        self.executor = SarvSystemExecutor()
        self.messaging = SarvMessagingBridge()
        self.control = SarvComputerControl()
        self.security = SarvAntiTheft()
        self.local_parser = SarvIntentParser()
        self.voice = SarvVoiceEngine()
        self.api_key = self.load_or_generate_key()

    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def load_or_generate_key(self) -> str:
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    data = json.load(f)
                    if data.get("api_key"):
                        return data["api_key"]
            except Exception:
                pass
        return self.request_new_key()

    def request_new_key(self) -> str:
        try:
            res = requests.post(
                f"{self.gateway_url}/v1/keys/generate",
                json={"client_name": "SARV-Desktop-Agent"},
                timeout=10
            )
            if res.status_code == 200:
                key = res.json().get("key_details", {}).get("api_key", "")
                with open(CONFIG_FILE, "w") as f:
                    json.dump({"api_key": key}, f, indent=2)
                return key
        except Exception as e:
            print(f" [KEY SYNC ERROR] {e}")
        return "sarv_live_fallback"

    def verify_connection(self) -> bool:
        try:
            res = requests.get(f"{self.gateway_url}/health", timeout=5)
            if res.status_code == 200:
                print(f"[ONLINE] Connected to SARV Gateway at {self.gateway_url}")
                return True
        except Exception:
            print(f"[LOCAL MODE] Running standalone offline core.")
            return True
        return False

    def execute_local_action(self, action: dict):
        action_type = action.get("action_type")
        target = action.get("target", "")
        params = action.get("parameters", {})

        if action_type == "LAUNCH_APP":
            self.executor.launch_application(target)
        elif action_type == "SEND_MESSAGE":
            self.messaging.send_whatsapp_message(target=target, message=params.get("content", ""))
        elif action_type == "LOCK_SYSTEM":
            self.control.lock_workstation()
        elif action_type == "VOLUME_UP":
            self.control.volume_up()
        elif action_type == "VOLUME_DOWN":
            self.control.volume_down()
        elif action_type == "MUTE":
            self.control.set_volume_mute()
        elif action_type == "TAKE_SCREENSHOT":
            self.control.take_screenshot()
        elif action_type == "SECURITY_SNAPSHOT":
            self.security.capture_intruder_snapshot()

    def process_command(self, command: str):
        if not command.strip():
            return

        # 1. Parse and execute local intents
        parsed = self.local_parser.parse_command(command)
        for action in parsed.get("actions", []):
            self.execute_local_action(action)

        response_text = ""
        # 2. Query Cloud Gateway
        try:
            res = requests.post(
                f"{self.gateway_url}/v1/execute",
                headers=self.get_headers(),
                json={"command": command},
                timeout=12
            )

            # Auto-heal on 401 expired key
            if res.status_code == 401:
                self.api_key = self.request_new_key()
                res = requests.post(
                    f"{self.gateway_url}/v1/execute",
                    headers=self.get_headers(),
                    json={"command": command},
                    timeout=12
                )

            if res.status_code == 200:
                response_text = res.json().get("result", "")
            else:
                response_text = parsed.get("speech_response", "")
        except Exception:
            response_text = parsed.get("speech_response", "")

        print(f"\n🤖 SARV: {response_text}")
        self.voice.speak(response_text)

    def run_cli_loop(self):
        print("=" * 65)
        print("  SARV AI OS - Sovereign Desktop Agent Active")
        print("  Commands: Type natural text | Type 'listen' for mic")
        print("  Type 'exit' to quit.")
        print("=" * 65)

        while True:
            try:
                cmd = input("\nSARV-Console >> ").strip()
                if cmd.lower() in ["exit", "quit"]:
                    break
                elif cmd.lower() == "listen":
                    spoken_cmd = self.voice.listen_command()
                    if spoken_cmd:
                        self.process_command(spoken_cmd)
                else:
                    self.process_command(cmd)
            except KeyboardInterrupt:
                break

if __name__ == "__main__":
    GATEWAY_HOST = "https://sarv-ai-os.onrender.com"
    agent = SarvDesktopAgent(gateway_url=GATEWAY_HOST)
    agent.verify_connection()
    agent.run_cli_loop()