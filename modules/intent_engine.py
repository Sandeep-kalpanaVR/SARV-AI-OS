import uuid
import re
from typing import Dict, Any, List

class SarvIntentParser:
    """Rule-based local intent engine for SARV AI OS."""
    def __init__(self):
        pass

    def parse_command(self, text: str) -> Dict[str, Any]:
        cmd_clean = text.lower().strip().rstrip("?.!")
        actions: List[Dict[str, Any]] = []
        step = 1

        if any(w in cmd_clean for w in ["what can you do", "capabilities", "features", "help", "commands"]):
            return {
                "request_id": f"req_{uuid.uuid4().hex[:8]}",
                "intent": "CAPABILITY_QUERY",
                "actions": [],
                "speech_response": (
                    "SARV AI OS Capabilities:\n"
                    "• WhatsApp & Email Communication Bridge\n"
                    "• Native Hardware Controls (Volume, Lock, Screenshot)\n"
                    "• Anti-Theft & Intrusion Surveillance Engine\n"
                    "• Desktop Application Launching\n"
                    "• Sovereign API Gateway & Unified Rate Limiter"
                )
            }

        if any(w in cmd_clean for w in ["who are you", "introduce yourself", "introduction", "what is sarv"]):
            return {
                "request_id": f"req_{uuid.uuid4().hex[:8]}",
                "intent": "IDENTITY_QUERY",
                "actions": [],
                "speech_response": "I am SARV AI OS—a sovereign, hybrid-ready AI Operating System."
            }

        if any(w in cmd_clean for w in ["who made you", "who created you", "developer"]):
            return {
                "request_id": f"req_{uuid.uuid4().hex[:8]}",
                "intent": "CREATOR_QUERY",
                "actions": [],
                "speech_response": "I was designed and developed by Sandeep as a sovereign AI Operating System."
            }

        if any(w in cmd_clean for w in ["message", "whatsapp", "text"]):
            match = re.search(r"(?:message|to)\s+([a-zA-Z0-9_+]+)\s*(?:saying|that|:)?\s*(.*)", text, re.IGNORECASE)
            target = match.group(1).strip() if match else "friend"
            body = match.group(2).strip() if (match and match.group(2)) else "Hello from SARV AI OS"
            actions.append({"step": step, "action_type": "SEND_MESSAGE", "target": target, "parameters": {"content": body}})
            step += 1

        if "lock" in cmd_clean and any(w in cmd_clean for w in ["pc", "system", "computer", "screen"]):
            actions.append({"step": step, "action_type": "LOCK_SYSTEM", "target": "os", "parameters": {}})
            step += 1

        if any(w in cmd_clean for w in ["volume", "sound", "mute"]):
            act = "MUTE" if "mute" in cmd_clean else ("VOLUME_UP" if "up" in cmd_clean else "VOLUME_DOWN")
            actions.append({"step": step, "action_type": act, "target": "audio", "parameters": {}})
            step += 1

        if "screenshot" in cmd_clean or "screen capture" in cmd_clean:
            actions.append({"step": step, "action_type": "TAKE_SCREENSHOT", "target": "screen", "parameters": {}})
            step += 1

        if any(w in cmd_clean for w in ["security", "intruder", "take photo", "camera"]):
            actions.append({"step": step, "action_type": "SECURITY_SNAPSHOT", "target": "camera", "parameters": {}})
            step += 1

        if "open" in cmd_clean or "launch" in cmd_clean:
            for app in ["vs code", "vscode", "chrome", "thonny", "terminal", "notepad"]:
                if app in cmd_clean:
                    actions.append({"step": step, "action_type": "LAUNCH_APP", "target": app, "parameters": {}})
                    step += 1

        return {
            "request_id": f"req_{uuid.uuid4().hex[:8]}",
            "intent": "MULTI_ACTION_EXECUTION" if actions else "KNOWLEDGE_QUERY",
            "actions": actions,
            "speech_response": f"Executing {len(actions)} system action(s) for command." if actions else f"SARV AI OS: Processed '{text}'"
        }
