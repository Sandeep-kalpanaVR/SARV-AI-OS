import sys
import os
import time
from collections import defaultdict
from typing import List, Optional, Dict, Any

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.key_manager import SarvKeyManager
from api.sarv_router import SarvAPIRouter
from config.settings import APP_NAME, VERSION

# Initialize App and Core Services
app = FastAPI(
    title=APP_NAME,
    version=VERSION,
    description="SARV AI OS Sovereign Cloud Gateway & Public API Engine"
)

# Enable CORS for public websites, extensions, and mobile apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

key_mgr = SarvKeyManager()
router = SarvAPIRouter()
security_scheme = HTTPBearer()

# In-Memory Rate Limiter Tracking
request_history = defaultdict(list)

def enforce_rate_limit(api_key: str, max_requests: int = 30, window_seconds: int = 60):
    now = time.time()
    request_history[api_key] = [t for t in request_history[api_key] if now - t < window_seconds]
    if len(request_history[api_key]) >= max_requests:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Maximum 30 requests per minute.")
    request_history[api_key].append(now)

def verify_sarv_key(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)):
    token = credentials.credentials
    is_valid, msg = key_mgr.validate_api_key(token)
    if not is_valid:
        raise HTTPException(status_code=401, detail=msg)
    enforce_rate_limit(token)
    return token

# Pydantic Request Models
class CommandRequest(BaseModel):
    command: str

class KeyGenRequest(BaseModel):
    client_name: str

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: Optional[str] = "sarv-ai-os"
    messages: List[ChatMessage]
    stream: Optional[bool] = False

# HTML Dashboard Interface
SARV_HTML_CONSOLE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SARV AI OS - Central Console</title>
    <style>
        :root {
            --bg-color: #0b0f19;
            --card-bg: #111827;
            --border-color: #1f2937;
            --accent-blue: #00f0ff;
            --accent-purple: #7000ff;
            --text-main: #f3f4f6;
            --text-dim: #9ca3af;
            --success: #10b981;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background-color: var(--bg-color); color: var(--text-main); padding: 20px; display: flex; justify-content: center; }
        .container { max-width: 900px; width: 100%; display: flex; flex-direction: column; gap: 20px; }
        .header { background: linear-gradient(135deg, #111827, #1f2937); border: 1px solid var(--accent-blue); padding: 20px; border-radius: 12px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 0 15px rgba(0, 240, 255, 0.2); }
        .header h1 { font-size: 24px; color: var(--accent-blue); letter-spacing: 2px; }
        .badge { background: rgba(16, 185, 129, 0.2); color: var(--success); border: 1px solid var(--success); padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; }
        .card { background: var(--card-bg); border: 1px solid var(--border-color); padding: 20px; border-radius: 12px; }
        .card h2 { font-size: 16px; color: var(--text-dim); margin-bottom: 12px; text-transform: uppercase; letter-spacing: 1px; }
        .input-group { display: flex; gap: 10px; margin-bottom: 10px; }
        input { flex: 1; background: #070a11; border: 1px solid var(--border-color); color: var(--text-main); padding: 12px; border-radius: 8px; font-size: 14px; outline: none; }
        input:focus { border-color: var(--accent-blue); }
        button { background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple)); border: none; color: white; padding: 12px 20px; border-radius: 8px; cursor: pointer; font-weight: bold; transition: opacity 0.2s; }
        button:hover { opacity: 0.9; }
        .terminal { background: #05070c; border: 1px solid var(--border-color); border-radius: 8px; padding: 15px; font-family: 'Courier New', Courier, monospace; font-size: 13px; color: #34d399; min-height: 180px; max-height: 300px; overflow-y: auto; white-space: pre-wrap; }
        .key-box { background: rgba(0, 240, 255, 0.1); border: 1px dashed var(--accent-blue); padding: 10px; border-radius: 6px; font-family: monospace; color: var(--accent-blue); word-break: break-all; display: none; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div>
                <h1>SARV AI OS</h1>
                <p style="color: var(--text-dim); font-size: 12px; margin-top: 4px;">Public Cloud Gateway & Sovereign API Engine</p>
            </div>
            <div class="badge">SYSTEM ONLINE</div>
        </div>

        <div class="card">
            <h2>1. Key Management</h2>
            <div class="input-group">
                <input type="text" id="clientName" placeholder="Client Name (e.g. JARVIS-Console)" value="JARVIS-MARK-XXXIX">
                <button onclick="generateKey()">Generate API Key</button>
            </div>
            <div id="keyDisplay" class="key-box"></div>
        </div>

        <div class="card">
            <h2>2. SARV Command Execution Console</h2>
            <div class="input-group">
                <input type="text" id="apiKeyInput" placeholder="Paste Active SARV API Key (sarv_live_...)">
            </div>
            <div class="input-group">
                <input type="text" id="commandInput" placeholder="Enter SARV command (e.g. Initiate diagnostic sequence)" onkeypress="handleKeyPress(event)">
                <button onclick="executeCommand()">Send Command</button>
            </div>
            <h2>Terminal Output</h2>
            <div class="terminal" id="terminal">[SARV OS READY] Public Gateway active. Enter API Key and send command...</div>
        </div>
    </div>

    <script>
        async function generateKey() {
            const clientName = document.getElementById('clientName').value || 'Default-Client';
            try {
                const response = await fetch('/v1/keys/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ client_name: clientName })
                });
                const data = await response.json();
                if(data.status === 'success') {
                    const apiKey = data.key_details.api_key;
                    document.getElementById('apiKeyInput').value = apiKey;
                    const keyBox = document.getElementById('keyDisplay');
                    keyBox.style.display = 'block';
                    keyBox.innerHTML = `<strong>New Generated Key:</strong> ${apiKey}`;
                    logTerminal(`[KEY GEN SUCCESS] Generated active key for '${clientName}'`);
                }
            } catch(err) {
                logTerminal(`[ERROR] Key generation failed: ${err.message}`);
            }
        }

        async function executeCommand() {
            const apiKey = document.getElementById('apiKeyInput').value.trim();
            const command = document.getElementById('commandInput').value.trim();

            if(!apiKey) {
                alert('Please enter or generate a SARV API Key first!');
                return;
            }
            if(!command) return;

            logTerminal(`> Executing: ${command}`);

            try {
                const response = await fetch('/v1/execute', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${apiKey}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ command: command })
                });
                
                const data = await response.json();
                if(response.ok) {
                    logTerminal(`🤖 SARV Response: ${data.result}`);
                } else {
                    logTerminal(`❌ Auth/Server Error (${response.status}): ${JSON.stringify(data.detail)}`);
                }
            } catch(err) {
                logTerminal(`❌ Connection Error: ${err.message}`);
            }
            document.getElementById('commandInput').value = '';
        }

        function logTerminal(text) {
            const term = document.getElementById('terminal');
            term.innerHTML += `\\n${text}`;
            term.scrollTop = term.scrollHeight;
        }

        function handleKeyPress(e) {
            if(e.key === 'Enter') executeCommand();
        }
    </script>
</body>
</html>"""

# API Routes
@app.get("/", response_class=HTMLResponse)
def get_root():
    return HTMLResponse(content=SARV_HTML_CONSOLE)

@app.get("/ui", response_class=HTMLResponse)
def get_ui():
    return HTMLResponse(content=SARV_HTML_CONSOLE)

@app.get("/health")
def health_check():
    return {"status": "ok", "app": APP_NAME, "version": VERSION}

@app.post("/v1/keys/generate")
def create_key(req: KeyGenRequest):
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

# Public OpenAI-Compatible Endpoint for Apps & Web Services
@app.post("/v1/chat/completions")
def chat_completions(req: ChatCompletionRequest, api_key: str = Depends(verify_sarv_key)):
    user_prompt = req.messages[-1].content if req.messages else ""
    sarv_response = router.process_request(api_key=api_key, command=user_prompt)
    
    return {
        "id": f"chatcmpl-sarv-{int(time.time())}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": "sarv-ai-os",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": sarv_response
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": len(user_prompt),
            "completion_tokens": len(sarv_response),
            "total_tokens": len(user_prompt) + len(sarv_response)
        }
    }