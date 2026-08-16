import os
import subprocess
from typing import Dict, Any

class SarvScreenProcessor:
    """
    Screen Awareness & Vision Processing Engine for SARV AI OS.
    Handles desktop captures and OCR text analysis.
    """
    def __init__(self, output_dir: str = "evidence/screen_captures"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def capture_screen(self, filename: str = "current_screen.png") -> str:
        """Captures active screen snapshot using native Windows GDI."""
        filepath = os.path.join(self.output_dir, filename)
        ps_cmd = (
            f"Add-Type -AssemblyName System.Windows.Forms; "
            f"[System.Windows.Forms.SendKeys]::SendWait('%{{PRTSC}}'); "
            f"$img = [System.Windows.Forms.Clipboard]::GetImage(); "
            f"if ($img) {{ $img.Save('{filepath}') }}"
        )
        try:
            subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True)
            print(f" [SCREEN PROCESSOR] Screen captured: {filepath}")
            return filepath
        except Exception as e:
            print(f" [SCREEN PROCESSOR ERROR] {e}")
            return ""

    def analyze_screen_context(self) -> Dict[str, Any]:
        """Captures screen and prepares it for vision inspection."""
        img_path = self.capture_screen()
        return {
            "status": "captured" if img_path else "failed",
            "image_path": img_path,
            "summary": "Active screen context captured."
        }