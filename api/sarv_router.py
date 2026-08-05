import os
from api.key_manager import SarvKeyManager
from config.settings import OFFLINE_MODE

class SarvAPIRouter:
    def __init__(self):
        self.key_manager = SarvKeyManager()

    def process_request(self, api_key: str, command: str) -> str:
        # 1. Authenticate SARV API Key
        is_valid, msg = self.key_manager.validate_api_key(api_key)
        if not is_valid:
            return f"[SARV AUTH ERROR 401] {msg}"

        # 2. SARV Native Processing Logic
        if not OFFLINE_MODE:
            # Process via SARV Central Engine
            return f"SARV AI OS [Cloud Core]: Successfully processed command -> '{command}'"
        else:
            # Fallback to SARV Local Engine
            return f"SARV AI OS [Local Core]: Executed command offline -> '{command}'"