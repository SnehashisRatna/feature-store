from pydantic import BaseModel

class RawTableCreate(BaseModel):
    name: str
    source_type: str
    location: str
    entity_column: str
