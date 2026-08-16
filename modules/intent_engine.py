import uuid
from typing import Dict, Any, List

class SarvIntentParser:
    """
    Rule-based local intent engine for SARV AI OS.
    Parses natural language commands into structured JSON actions and natural speech responses.
    """
    def __init__(self):
        pass

    def parse_command(self, text: str) -> Dict[str, Any]:
        cmd_clean = text.lower().strip().rstrip("?.!")
        actions: List[Dict[str, Any]] = []
        step = 1

        # 1. Capability Queries
        if any(w in cmd_clean for w in ["what can you do", "capabilities", "features", "help", "commands"]):
            return {
                "request_id": f"req_{uuid.uuid4().hex[:8]}",
                "intent": "CAPABILITY_QUERY",
                "actions": [],
                "speech_response": (
                    "SARV AI OS Capabilities:\n"
                    "• Sovereign API Gateway & Unified Key Management\n"
                    "• Rule-based intent parsing & local JSON execution\n"
                    "• Desktop application launching & diagnostic checks\n"
                    "• Offline fallback & hybrid cloud routing"
                )
            }

        # 2. Identity / Intro Queries
        if any(w in cmd_clean for w in ["who are you", "introduce yourself", "introduction", "what is sarv"]):
            return {
                "request_id": f"req_{uuid.uuid4().hex[:8]}",
                "intent": "IDENTITY_QUERY",
                "actions": [],
                "speech_response": (
                    "I am SARV AI OS—a sovereign, hybrid-ready AI Operating System "
                    "built for modular cloud routing, desktop execution, and controller hardware integration."
                )
            }

        # 3. Application Launch Commands
        if "open" in cmd_clean or "launch" in cmd_clean:
            apps = ["vs code", "chrome", "thonny", "terminal", "notepad"]
            for app in apps:
                if app in cmd_clean:
                    actions.append({
                        "step": step,
                        "action_type": "LAUNCH_APP",
                        "target": app,
                        "parameters": {}
                    })
                    step += 1

        # 4. System / Router Diagnostics
        if any(w in cmd_clean for w in ["check", "status", "diagnostic", "health", "ping"]):
            actions.append({
                "step": step,
                "action_type": "NETWORK_DIAGNOSTIC",
                "target": "cloud_router",
                "parameters": {"endpoint": "/health"}
            })
            step += 1

        # Execution or General Response
        if actions:
            intent_type = "MULTI_ACTION_EXECUTION"
            speech_resp = f"Executing {len(actions)} system action(s) for command."
        else:
            intent_type = "KNOWLEDGE_QUERY"
            speech_resp = f"SARV AI OS processed request: '{text}'"

        return {
            "request_id": f"req_{uuid.uuid4().hex[:8]}",
            "intent": intent_type,
            "actions": actions,
            "speech_response": speech_resp
        }