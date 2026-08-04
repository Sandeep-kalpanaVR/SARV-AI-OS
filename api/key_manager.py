import os
import json
import secrets
import hashlib
from datetime import datetime

KEYS_FILE = os.path.join("config", "api_keys.json")

class SarvKeyManager:
    def __init__(self):
        os.makedirs("config", exist_ok=True)
        if not os.path.exists(KEYS_FILE):
            self._save_db({})

    def _load_db(self) -> dict:
        try:
            with open(KEYS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def _save_db(self, db: dict):
        with open(KEYS_FILE, "w", encoding="utf-8") as f:
            json.dump(db, f, indent=4)

    def _hash_key(self, raw_key: str) -> str:
        """Hash raw API key using SHA-256 for secure local storage."""
        return hashlib.sha256(raw_key.encode()).hexdigest()

    def generate_api_key(self, client_name: str, key_type: str = "live") -> dict:
        """Generates a new secure SARV API Key formatted as sarv_live_<hash>."""
        token = secrets.token_hex(24)
        raw_key = f"sarv_{key_type}_{token}"
        hashed_key = self._hash_key(raw_key)

        db = self._load_db()
        db[hashed_key] = {
            "client_name": client_name,
            "key_type": key_type,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "active"
        }
        self._save_db(db)

        return {
            "client_name": client_name,
            "api_key": raw_key,
            "status": "active"
        }

    def validate_api_key(self, raw_key: str) -> tuple[bool, str]:
        """Validates incoming SARV API Key requests."""
        if not raw_key or not raw_key.startswith("sarv_"):
            return False, "Invalid SARV API Key format"

        hashed_key = self._hash_key(raw_key)
        db = self._load_db()

        if hashed_key in db:
            key_data = db[hashed_key]
            if key_data.get("status") == "active":
                return True, f"Authenticated: '{key_data['client_name']}'"
            return False, "API key has been revoked"

        return False, "Invalid or unrecognized SARV API Key"