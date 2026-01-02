from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base

class FeatureValue(Base):
    __tablename__ = "feature_values"

    id = Column(Integer, primary_key=True)
    entity_id = Column(String, nullable=False)
    feature_id = Column(Integer, ForeignKey("features.id"))
    version = Column(Integer, nullable=False)
    value = Column(Float, nullable=False)
