import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.intent_engine import SarvIntentParser

class SarvAPIRouter:
    def __init__(self):
        self.intent_parser = SarvIntentParser()

    def process_request(self, api_key: str, command: str) -> str:
        # Normalize command string for matching
        cmd = command.lower().strip().rstrip("?.!")

        # Direct Conversational / Capability Triggers
        if "what can you do" in cmd or "capabilities" in cmd or "features" in cmd:
            return (
                "SARV AI OS Capabilities:\n"
                "• Unified Sovereign API Gateway & Key Management\n"
                "• Rule-based intent parsing & local execution schema\n"
                "• Desktop application launching & diagnostic checks\n"
                "• Local offline fallback & hybrid cloud routing"
            )

        if "who are you" in cmd or "introduce yourself" in cmd or "introduction" in cmd:
            return (
                "I am SARV AI OS—a sovereign, hybrid-ready AI Operating System "
                "built for modular cloud routing, desktop execution, and controller hardware integration."
            )

        # Rule-based intent parser fallback
        parsed = self.intent_parser.parse_command(command)
        if parsed.get("actions") and len(parsed["actions"]) > 0:
            return f"Executing {len(parsed['actions'])} action(s): {parsed['speech_response']}"
        
        return parsed.get("speech_response", f"SARV AI OS [Local Core]: Executed command -> '{command}'")