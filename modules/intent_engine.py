import re
import uuid
from typing import Dict, Any, List

class SarvIntentParser:
    """
    Rule-based local intent engine for SARV AI OS.
    Parses natural language commands into structured JSON actions.
    """
    def __init__(self):
        pass

    def parse_command(self, text: str) -> Dict[str, Any]:
        command_lower = text.lower().strip()
        actions: List[Dict[str, Any]] = []
        step = 1

        # Check for launch commands
        if "open" in command_lower or "launch" in command_lower:
            apps = ["vs code", "chrome", "thonny", "terminal", "notepad"]
            for app in apps:
                if app in command_lower:
                    actions.append({
                        "step": step,
                        "action_type": "LAUNCH_APP",
                        "target": app,
                        "parameters": {}
                    })
                    step += 1

        # Check for diagnostic or status checks
        if "check" in command_lower or "status" in command_lower or "diagnostic" in command_lower:
            actions.append({
                "step": step,
                "action_type": "NETWORK_DIAGNOSTIC",
                "target": "cloud_router",
                "parameters": {"endpoint": "/health"}
            })
            step += 1

        # Default fallback if no specific action pattern matched
        if not actions:
            intent_type = "KNOWLEDGE_QUERY"
            speech_resp = f"SARV AI OS processed request: '{text}'"
        else:
            intent_type = "MULTI_ACTION_EXECUTION"
            speech_resp = f"Executing {len(actions)} system actions for command."

        return {
            "request_id": f"req_{uuid.uuid4().hex[:8]}",
            "intent": intent_type,
            "actions": actions,
            "speech_response": speech_resp
        }