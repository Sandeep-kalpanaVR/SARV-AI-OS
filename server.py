import sys
import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.key_manager import SarvKeyManager
from api.sarv_router import SarvAPIRouter
from config.settings import APP_NAME, VERSION

app = FastAPI(
    title=APP_NAME,
    version=VERSION,
    description="SARV AI OS Central Cloud & Offline API Router"
)

key_mgr = SarvKeyManager()
router = SarvAPIRouter()
security_scheme = HTTPBearer()

class CommandRequest(BaseModel):
    command: str

class KeyGenRequest(BaseModel):
    client_name: str

def verify_sarv_key(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)):
    token = credentials.credentials
    is_valid, msg = key_mgr.validate_api_key(token)
    if not is_valid:
        raise HTTPException(status_code=401, detail=msg)
    return token

@app.get("/")
def root():
    return {
        "status": "online",
        "system": APP_NAME,
        "version": VERSION,
        "message": "SARV AI OS Web Server is active."
    }

@app.post("/v1/keys/generate")
def create_key(req: KeyGenRequest):
    """
    Public endpoint to generate a fresh SARV API Key on the cloud server.
    """
    key_info = key_mgr.generate_api_key(client_name=req.client_name, key_type="live")
    return {
        "status": "success",
        "key_details": key_info
    }

@app.post("/v1/execute")
def execute_command(req: CommandRequest, api_key: str = Depends(verify_sarv_key)):
    response = router.process_request(api_key=api_key, command=req.command)
    return {
        "status": "success",
        "command": req.command,
        "result": response
    }