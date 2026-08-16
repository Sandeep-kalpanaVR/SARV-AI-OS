import os
import subprocess
import shutil
from typing import Dict, Any, List

class SarvSystemExecutor:
    def __init__(self):
        self.app_map = {
            "vs code": ["code"],
            "vscode": ["code"],
            "thonny": ["thonny", os.path.expandvars(r"%LOCALAPPDATA%\Programs\Thonny\thonny.exe"), r"C:\Program Files\Thonny\thonny.exe"],
            "chrome": ["chrome", r"C:\Program Files\Google\Chrome\Application\chrome.exe"],
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
