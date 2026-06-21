from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

logs_storage = []


class LogEntry(BaseModel):
    message: str
    level: str
    source: str


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/logs")
def create_log(entry: LogEntry):
    log = entry.model_dump()
    log["timestamp"] = datetime.now().isoformat()
    logs_storage.append(log)
    return {"status": "created", "log": log}


@app.get("/logs")
def get_logs():
    return {"count": len(logs_storage), "logs": logs_storage}
