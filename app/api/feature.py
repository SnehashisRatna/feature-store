from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.feature import Feature
from app.models.raw_table import RawTable
from app.schemas.feature import FeatureCreate, FeatureCompute
from app.services.feature_store import create_feature_version, get_feature_vector

router = APIRouter(prefix="/feature", tags=["Features"])

@router.post("/register")
def register_feature(data: FeatureCreate, db: Session = Depends(get_db)):
    feature = Feature(**data.dict())
    db.add(feature)
    db.commit()
    db.refresh(feature)
    return feature


@router.post("/compute")
def compute_feature_api(data: FeatureCompute, db: Session = Depends(get_db)):
    feature = db.query(Feature).get(data.feature_id)
    raw_table = db.query(RawTable).get(feature.raw_table_id)
    version = create_feature_version(db, feature, raw_table, data.logic)
    return {"feature_id": feature.id, "version": version}


@router.get("/vector/{entity_id}")
def get_features(entity_id: str, features: str, db: Session = Depends(get_db)):
    feature_list = features.split(",")
    return get_feature_vector(db, entity_id, feature_list)
