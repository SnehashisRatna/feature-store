from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime
from datetime import datetime
from app.database import Base

class FeatureVersion(Base):
    __tablename__ = "feature_versions"

    id = Column(Integer, primary_key=True)
    feature_id = Column(Integer, ForeignKey("features.id"))
    version = Column(Integer, nullable=False)
    logic = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
