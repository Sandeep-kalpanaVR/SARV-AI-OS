import sys
import os
from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel

# Add current folder to path dynamically
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

class CommandRequest(BaseModel):
    command: str

def verify_sarv_key(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing.")
    
    token = authorization.replace("Bearer ", "").strip()
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

@app.post("/v1/execute")
def execute_command(req: CommandRequest, api_key: str = Depends(verify_sarv_key)):
    response = router.process_request(api_key=api_key, command=req.command)
    return {
        "status": "success",
        "command": req.command,
        "result": response
    }