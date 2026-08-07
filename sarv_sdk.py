import requests
from typing import Dict, Any

class SarvClient:
    """
    Sovereign Client SDK for SARV AI OS.
    Uses only SARV API Key authentication.
    """
    def __init__(self, api_key: str, base_url: str = "https://sarv-ai-os.onrender.com"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    @staticmethod
    def generate_key(client_name: str, base_url: str = "https://sarv-ai-os.onrender.com") -> Dict[str, Any]:
        url = f"{base_url.rstrip('/')}/v1/keys/generate"
        response = requests.post(url, json={"client_name": client_name})
        response.raise_for_status()
        return response.json()

    def execute(self, command: str) -> Dict[str, Any]:
        url = f"{self.base_url}/v1/execute"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {"command": command}
        
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 401:
            return {"status": "error", "message": "Unauthorized: Invalid SARV API Key"}
        
        response.raise_for_status()
        return response.json()