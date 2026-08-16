import os
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
