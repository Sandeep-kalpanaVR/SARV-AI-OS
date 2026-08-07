import subprocess
import os
import sys
import webbrowser
from typing import List, Dict, Any

class SarvSystemExecutor:
    """
    Executes structured JSON action lists directly on the host OS.
    """
    def __init__(self):
        self.os_type = sys.platform

    def execute_actions(self, actions_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        
        for action in actions_list:
            action_type = action.get("action_type")
            target = action.get("target", "").lower()
            step = action.get("step")

            try:
                if action_type == "LAUNCH_APP":
                    status = self._launch_application(target)
                    results.append({"step": step, "target": target, "status": status})

                elif action_type == "NETWORK_DIAGNOSTIC":
                    results.append({"step": step, "target": target, "status": "diagnostic_ping_ready"})

                else:
                    results.append({"step": step, "target": target, "status": "unknown_action_type"})

            except Exception as e:
                results.append({"step": step, "target": target, "status": f"error: {str(e)}"})

        return results

    def _launch_application(self, target: str) -> str:
        if "chrome" in target:
            webbrowser.open("https://google.com")
            return "opened_browser"
            
        elif "vs code" in target or "code" in target:
            cmd = "code" if self.os_type != "win32" else "code.cmd"
            subprocess.Popen([cmd], shell=True)
            return "launched_vs_code"

        elif "notepad" in target and self.os_type == "win32":
            subprocess.Popen(["notepad.exe"])
            return "launched_notepad"

        return f"unrecognized_app_{target}"