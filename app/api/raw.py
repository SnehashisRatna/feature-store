from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.raw_table import RawTable
from app.schemas.raw import RawTableCreate

router = APIRouter(prefix="/raw", tags=["Raw Tables"])

@router.post("/register")
def register_raw_table(data: RawTableCreate, db: Session = Depends(get_db)):
    raw = RawTable(**data.dict())
    db.add(raw)
    db.commit()
    db.refresh(raw)
    return raw
