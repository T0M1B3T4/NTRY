from datetime import datetime
from fastapi import FastAPI, Request
from pydantic import BaseModel
import json

app = FastAPI()

class LoginRequest(BaseModel):
    username: str
    password: str


@app.get("/")
def health_check():
    return {
        "status": "running",
        "service": "backend"
    }

@app.post("/login")
async def login(data: LoginRequest, request: Request):

    VALID_USERS = { 
       "admin": "admin123",
       "developer": "dev123",
       "guest": "guest123"
    }
    
    success = (
        data.username in VALID_USERS
        and VALID_USERS[data.username] == data.password
    )

    client_ip = request.headers.get(
        "X-Forwarded-For",
        request.client.host
    )

    log_event = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": "login_attempt",
        "ip": client_ip,
        "username": data.username,
        "success": success
    }

    with open("/data/raw/login_logs.jsonl", "a") as file:
           file.write(json.dumps(log_event) + "\n"),

    return {
        "message": "Login processed",
        "success": success
    }