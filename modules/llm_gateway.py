import os
import requests
from typing import Optional

class SarvLLMGateway:
    """
    Centralized Cloud LLM Fallback Engine.
    Abstracts upstream model providers behind the sovereign SARV architecture.
    """
    def __init__(self):
        # You can set upstream provider key in Render environment variables or .env
        self.provider_api_key = os.getenv("UPSTREAM_API_KEY", "")
        self.provider_url = os.getenv(
            "UPSTREAM_ENDPOINT", 
            "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
        )

    def generate_response(self, prompt: str) -> str:
        """Sends query to upstream model provider or returns fallback response."""
        if not self.provider_api_key:
            return (
                f"SARV Core: '{prompt}' received. "
                "Cloud LLM upstream key is not configured on the gateway. "
                "Local intent and system execution remain fully active."
            )

        headers = {
            "Authorization": f"Bearer {self.provider_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "inputs": f"<s>[INST] You are SARV AI OS, a sleek, authoritative system intelligence. Answer clearly and concisely: {prompt} [/INST]",
            "parameters": {"max_new_tokens": 250, "temperature": 0.7}
        }

        try:
            response = requests.post(self.provider_url, headers=headers, json=payload, timeout=12)
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    text = result[0].get("generated_text", "")
                    # Strip out prompt prefix if present
                    if "[/INST]" in text:
                        text = text.split("[/INST]")[-1].strip()
                    return text
            return f"SARV Gateway Notice: Upstream responded with status {response.status_code}."
        except Exception as e:
            return f"SARV Hybrid Fallback: Upstream query timed out ({str(e)}). Running in local mode."