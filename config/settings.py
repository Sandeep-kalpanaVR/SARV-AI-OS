import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = "SARV AI OS"
VERSION = "1.0.0"

# Server Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
OFFLINE_MODE = os.getenv("OFFLINE_MODE", "False").lower() in ("true", "1", "t")

# API Endpoints
SARV_BASE_URL = os.getenv("SARV_BASE_URL", "https://sarv-ai-os.onrender.com")