from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from src.db.database import Base


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True)
    message = Column(String, nullable=False)
    level = Column(String, nullable=False)
    source = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)
