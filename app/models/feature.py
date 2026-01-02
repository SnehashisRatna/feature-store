from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Feature(Base):
    __tablename__ = "features"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    entity = Column(String, nullable=False)
    raw_table_id = Column(Integer, ForeignKey("raw_tables.id"))
    description = Column(String)
