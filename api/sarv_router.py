import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.intent_engine import SarvIntentParser

class SarvAPIRouter:
    def __init__(self):
        self.intent_parser = SarvIntentParser()

    def process_request(self, api_key: str, command: str) -> str:
        # Route command directly through the Intent Parser
        parsed = self.intent_parser.parse_command(command)
        return parsed.get("speech_response", f"SARV AI OS: Processed '{command}'")