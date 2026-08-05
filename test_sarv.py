import requests

SARV_URL = "https://sarv-ai-os.onrender.com"

# 1. Get SARV Key
key_res = requests.post(f"{SARV_URL}/v1/keys/generate", json={"client_name": "JARVIS-MARK-XXXIX"}).json()
sarv_key = key_res["key_details"]["api_key"]

print(f"🔑 Active SARV Key: {sarv_key}")

# 2. Execute Command on SARV OS
headers = {"Authorization": f"Bearer {sarv_key}"}
payload = {"command": "Initiate JARVIS core diagnostic sequence"}

res = requests.post(f"{SARV_URL}/v1/execute", json=payload, headers=headers)
print("\n🤖 SARV Output:", res.json()["result"])