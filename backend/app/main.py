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

    log_event = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": "login_attempt",
        "ip": request.client.host,
        "username": data.username,
        "success": False
    }

    with open("login_logs.jsonl", "a") as file:
        file.write(json.dumps(log_event))

    return {
        "message": "Login processed",
        "success": False
    }