from api.key_manager import SarvKeyManager
from config.settings import OFFLINE_MODE

class SarvAPIRouter:
    def __init__(self):
        self.key_manager = SarvKeyManager()

    def process_request(self, api_key: str, command: str) -> str:
        # 1. Authenticate incoming API Key
        is_valid, msg = self.key_manager.validate_api_key(api_key)
        if not is_valid:
            return f"[SARV AUTH ERROR 401] {msg}"

        # 2. Execute request upon successful authentication
        if OFFLINE_MODE:
            return f"[{msg}] Executed Locally: {command}"
        else:
            return f"[{msg}] Executed via SARV Cloud: {command}"