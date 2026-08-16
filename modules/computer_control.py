import os
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
