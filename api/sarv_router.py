import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.intent_engine import SarvIntentParser
from modules.llm_gateway import SarvLLMGateway

class SarvAPIRouter:
    def __init__(self):
        self.intent_parser = SarvIntentParser()
        self.llm_gateway = SarvLLMGateway()

    def process_request(self, api_key: str, command: str) -> str:
        # 1. Parse for local commands & fixed system intents
        parsed = self.intent_parser.parse_command(command)
        
        # If it's a specific system action, identity, or capability query, return immediately
        if parsed.get("intent") in ["CAPABILITY_QUERY", "IDENTITY_QUERY", "MULTI_ACTION_EXECUTION"]:
            return parsed.get("speech_response")

        # 2. Open-ended queries -> route through the Cloud LLM Gateway
        return self.llm_gateway.generate_response(command)