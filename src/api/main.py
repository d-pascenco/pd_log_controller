from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.db.database import engine, get_db, Base
from src.db.models import Log

Base.metadata.create_all(bind=engine)
app = FastAPI()

class LogEntry(BaseModel):
    message: str
    level: str
    source: str

def format_timestamp(ts):
    return ts.strftime('%Y-%m-%d %H:%M:%S.%f')

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/logs")
def create_log(entry: LogEntry, db: Session = Depends(get_db)):
    log = Log(message=entry.message, level=entry.level, source=entry.source)
    db.add(log)
    db.commit()
    db.refresh(log)
    return {"status": "created", "log": {
        "id": log.id,
        "source": log.source,
        "timestamp": format_timestamp(log.timestamp),
        "level": log.level,
        "message": log.message
    }}

@app.get("/logs")
def get_logs(db: Session = Depends(get_db)):
    logs = db.query(Log).all()
    return {"count": len(logs), "logs": [
        {
            "id": log.id,
            "source": log.source,
            "timestamp": format_timestamp(log.timestamp),
            "level": log.level,
            "message": log.message
        }
        for log in logs
    ]}
