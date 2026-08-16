import os

FILES = {
    # 1. Computer & Environment Controls
    "modules/computer_control.py": '''import os
import sys
import ctypes
import subprocess
from typing import Dict, Any

class SarvComputerControl:
    """Hardware and OS Level Controls for Windows Desktop."""
    def __init__(self):
        pass

    def lock_workstation(self) -> bool:
        ctypes.windll.user32.LockWorkStation()
        return True

    def set_volume_mute(self) -> bool:
        ctypes.windll.user32.keybd_event(0xAD, 0, 0, 0)
        ctypes.windll.user32.keybd_event(0xAD, 0, 2, 0)
        return True

    def volume_up(self, steps: int = 5) -> bool:
        for _ in range(steps):
            ctypes.windll.user32.keybd_event(0xAF, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0xAF, 0, 2, 0)
        return True

    def volume_down(self, steps: int = 5) -> bool:
        for _ in range(steps):
            ctypes.windll.user32.keybd_event(0xAE, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0xAE, 0, 2, 0)
        return True

    def take_screenshot(self, output_path: str = "screenshot.png") -> str:
        ps_cmd = (
            f"Add-Type -AssemblyName System.Windows.Forms; "
            f"[System.Windows.Forms.SendKeys]::SendWait('%{{PRTSC}}'); "
            f"$img = [System.Windows.Forms.Clipboard]::GetImage(); "
            f"if ($img) {{ $img.Save('{output_path}') }}"
        )
        try:
            subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True)
            return output_path
        except Exception as e:
            print(f" [SCREENSHOT ERROR] {e}")
            return ""
''',

    # 2. Anti-Theft & Intrusion Security
    "modules/anti_theft.py": '''import os
import time
import cv2

class SarvAntiTheft:
    """Surveillance & Intruder Snapshot Engine."""
    def __init__(self, evidence_dir: str = "evidence/anti_theft"):
        self.evidence_dir = evidence_dir
        os.makedirs(self.evidence_dir, exist_ok=True)

    def capture_intruder_snapshot(self) -> str:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(self.evidence_dir, f"intruder_{timestamp}.jpg")

        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not cap.isOpened():
            cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print(" [SECURITY ERROR] Could not access camera.")
            return ""

        for _ in range(5):
            ret, frame = cap.read()

        if ret and frame is not None:
            cv2.imwrite(filepath, frame)
            print(f" [SECURITY EVIDENCE] Snapshot saved to: {filepath}")
        else:
            filepath = ""

        cap.release()
        return filepath
''',

    # 3. Messaging Bridge
    "modules/messaging_bridge.py": '''import os
import urllib.parse
import webbrowser
from typing import Dict, Any

class SarvMessagingBridge:
    """Automated Communication & Messaging Engine for SARV AI OS."""
    def __init__(self):
        self.contacts = {
            "dad": "+91XXXXXXXXXX",
            "friend": "+91XXXXXXXXXX"
        }

    def resolve_contact(self, name_or_number: str) -> str:
        return self.contacts.get(name_or_number.lower().strip(), name_or_number)

    def send_whatsapp_message(self, target: str, message: str) -> Dict[str, Any]:
        phone = self.resolve_contact(target)
        phone_clean = "".join([c for c in phone if c.isdigit() or c == '+'])
        encoded_message = urllib.parse.quote(message)

        if phone_clean:
            url = f"https://web.whatsapp.com/send?phone={phone_clean}&text={encoded_message}"
        else:
            url = f"https://web.whatsapp.com/send?text={encoded_message}"

        print(f" [MESSAGING] Dispatching WhatsApp payload to '{target}'...")
        webbrowser.open(url)
        return {"status": "success", "platform": "whatsapp", "target": target}
''',

    # 4. Intent Engine
    "modules/intent_engine.py": '''import uuid
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
                    "SARV AI OS Capabilities:\\n"
                    "• WhatsApp & Email Communication Bridge\\n"
                    "• Native Hardware Controls (Volume, Lock, Screenshot)\\n"
                    "• Anti-Theft & Intrusion Surveillance Engine\\n"
                    "• Desktop Application Launching\\n"
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
            match = re.search(r"(?:message|to)\\s+([a-zA-Z0-9_+]+)\\s*(?:saying|that|:)?\\s*(.*)", text, re.IGNORECASE)
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
''',

    # 5. System Executor
    "modules/system_executor.py": '''import os
import subprocess
import shutil
from typing import Dict, Any, List

class SarvSystemExecutor:
    def __init__(self):
        self.app_map = {
            "vs code": ["code"],
            "vscode": ["code"],
            "thonny": ["thonny", os.path.expandvars(r"%LOCALAPPDATA%\\Programs\\Thonny\\thonny.exe"), r"C:\\Program Files\\Thonny\\thonny.exe"],
            "chrome": ["chrome", r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"],
            "notepad": ["notepad.exe"],
            "terminal": ["wt.exe", "powershell.exe", "cmd.exe"]
        }

    def launch_application(self, target_app: str) -> bool:
        target = target_app.lower().strip()
        candidates = self.app_map.get(target, [target])
        for candidate in candidates:
            if shutil.which(candidate):
                subprocess.Popen([candidate], shell=True)
                print(f" [EXECUTOR] Launched: {candidate}")
                return True
            elif os.path.exists(candidate):
                subprocess.Popen([candidate])
                print(f" [EXECUTOR] Launched binary: {candidate}")
                return True
        try:
            os.system(f"start {target}")
            return True
        except Exception as e:
            print(f" [EXECUTOR ERROR] {e}")
            return False
'''
}

def generate_tree():
    for filepath, content in FILES.items():
        dir_name = os.path.dirname(filepath)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Generated: {filepath}")

    print("\n✨ All SARV AI OS modules generated successfully!")

if __name__ == "__main__":
    generate_tree()