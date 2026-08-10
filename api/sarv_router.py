import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.intent_engine import SarvIntentParser

class SarvAPIRouter:
    def __init__(self):
        self.intent_parser = SarvIntentParser()

    def process_request(self, api_key: str, command: str) -> str:
        cmd = command.lower().strip()

        # Direct Conversational / Capability Triggers
        if "what can you do" in cmd or "capabilities" in cmd or "features" in cmd:
            return (
                "SARV AI OS Capabilities:\n"
                "• Unified API Gateway & Key Management\n"
                "• Rule-based intent parsing & execution schema\n"
                "• Desktop application launching & diagnostic checks\n"
                "• Local offline fallback processing"
            )

        if "who are you" in cmd or "introduce yourself" in cmd:
            return (
                "I am SARV AI OS—a sovereign, hybrid-ready AI Operating System "
                "built for modular cloud routing, desktop execution, and controller hardware integration."
            )

        # Rule-based intent parser fallback
        parsed = self.intent_parser.parse_command(command)
        if parsed.get("actions"):
            return f"Executing {len(parsed['actions'])} action(s): {parsed['speech_response']}"
        
        return parsed.get("speech_response", f"SARV AI OS: Processed '{command}'")