from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class RawTable(Base):
    __tablename__ = "raw_tables"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    source_type = Column(String, nullable=False)
    location = Column(String, nullable=False)
    entity_column = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    