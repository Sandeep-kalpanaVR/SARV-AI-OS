import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.intent_engine import SarvIntentParser

class SarvAPIRouter:
    def __init__(self):
        self.intent_parser = SarvIntentParser()

    def process_request(self, api_key: str, command: str) -> str:
        command_lower = command.lower().strip()

        # Custom System Response for Introductions
        if "introduce yourself" in command_lower or "who are you" in command_lower:
            return (
                "Greetings. I am SARV AI OS—a sovereign, hybrid-ready AI Operating System "
                "designed for modular desktop execution, cloud routing, and local hardware control."
            )

        # Custom System Response for Capabilities
        if "what can you do" in command_lower or "capabilities" in command_lower:
            return (
                "SARV AI OS Capabilities:\n"
                "1. Sovereign API Gateway & OpenAI-compatible endpoints\n"
                "2. Rule-based intent parsing & local JSON schema generation\n"
                "3. Desktop OS application launching & diagnostic checks\n"
                "4. Offline fallback execution when network connectivity drops"
            )

        # Standard Intent Engine Processing
        parsed = self.intent_parser.parse_command(command)
        return parsed.get("speech_response", f"SARV AI OS [Local Core]: Executed command -> '{command}'")