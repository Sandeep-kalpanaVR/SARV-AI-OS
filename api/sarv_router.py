import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.intent_engine import SarvIntentParser

class SarvAPIRouter:
    def __init__(self):
        self.intent_parser = SarvIntentParser()

    def process_request(self, api_key: str, command: str) -> str:
        # Clean and normalize the command string
        cmd = command.lower().strip().rstrip("?.!")

        # 1. Broad matching for capability questions
        if any(phrase in cmd for phrase in ["what can you do", "capabilities", "features", "help", "commands"]):
            return (
                "SARV AI OS Capabilities:\n"
                "• Sovereign API Gateway & Key Management\n"
                "• Rule-based intent parsing & execution schema\n"
                "• Desktop application launching & system diagnostics\n"
                "• Local offline fallback & hybrid cloud routing"
            )

        # 2. Broad matching for introduction questions
        if any(phrase in cmd for phrase in ["who are you", "introduce yourself", "introduction", "what is sarv"]):
            return (
                "I am SARV AI OS—a sovereign, hybrid-ready AI Operating System "
                "built for modular cloud routing, desktop execution, and controller hardware integration."
            )

        # 3. Fallback to local intent parser module
        parsed = self.intent_parser.parse_command(command)
        if parsed.get("actions") and len(parsed["actions"]) > 0:
            return f"Executing {len(parsed['actions'])} action(s): {parsed['speech_response']}"
        
        # 4. Default clean conversational response
        return f"SARV AI OS processed request: '{command}'"