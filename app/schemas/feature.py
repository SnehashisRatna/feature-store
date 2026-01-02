from pydantic import BaseModel

class FeatureCreate(BaseModel):
    name: str
    entity: str
    raw_table_id: int
    description: str | None = None

class FeatureCompute(BaseModel):
    feature_id: int
    logic: str

