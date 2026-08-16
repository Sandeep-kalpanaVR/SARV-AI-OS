import os
import urllib.parse
import webbrowser
from typing import Dict, Any

class SarvMessagingBridge:
    """Automated Communication & Messaging Engine for SARV AI OS."""
    def __init__(self):
        self.contacts = {
            "dad": "+91XXXXXXXXXX",
            "friend": "+91XXXXXXXXXX"
        }

    def resolve_contact(self, name_or_number: str) -> str:
        return self.contacts.get(name_or_number.lower().strip(), name_or_number)

    def send_whatsapp_message(self, target: str, message: str) -> Dict[str, Any]:
        phone = self.resolve_contact(target)
        phone_clean = "".join([c for c in phone if c.isdigit() or c == '+'])
        encoded_message = urllib.parse.quote(message)

        if phone_clean:
            url = f"https://web.whatsapp.com/send?phone={phone_clean}&text={encoded_message}"
        else:
            url = f"https://web.whatsapp.com/send?text={encoded_message}"

        print(f" [MESSAGING] Dispatching WhatsApp payload to '{target}'...")
        webbrowser.open(url)
        return {"status": "success", "platform": "whatsapp", "target": target}
