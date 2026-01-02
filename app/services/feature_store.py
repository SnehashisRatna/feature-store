from app.services.feature_compute import compute_feature
from app.models.feature import Feature
from app.models.feature_version import FeatureVersion
from app.models.feature_value import FeatureValue
from fastapi import HTTPException


FEATURE_CACHE = {}


def create_feature_version(db, feature, raw_table, logic):
    """
    Creates a new version of a feature and stores computed values.
    """

    # 1️⃣ Fetch latest version
    latest = (
        db.query(FeatureVersion)
        .filter(FeatureVersion.feature_id == feature.id)
        .order_by(FeatureVersion.version.desc())
        .first()
    )

    # 2️⃣ Determine new version number
    new_version = 1 if not latest else latest.version + 1

    # 3️⃣ Store feature version metadata
    feature_version = FeatureVersion(
        feature_id=feature.id,
        version=new_version,
        logic=logic
    )
    db.add(feature_version)
    db.commit()

    # 4️⃣ Compute feature values using Pandas
    values = compute_feature(raw_table, logic)

    # 5️⃣ Store computed feature values
    for entity_id, value in values.items():
        db.add(
            FeatureValue(
                entity_id=str(entity_id),
                feature_id=feature.id,
                version=new_version,
                value=float(value)
            )
        )

    db.commit()

    # 6️⃣ Invalidate cache to avoid stale reads
    FEATURE_CACHE.clear()

    return new_version

def get_feature_vector(db, entity_id, feature_names):
    feature_vector = {}

    for name in feature_names:
        cache_key = (str(entity_id), name)

        # 1️⃣ Cache check
        if cache_key in FEATURE_CACHE:
            feature_vector[name] = FEATURE_CACHE[cache_key]
            continue

        # 2️⃣ Validate feature exists
        feature = db.query(Feature).filter(Feature.name == name).first()
        if not feature:
            raise HTTPException(
                status_code=404,
                detail=f"Feature '{name}' not found"
            )

        # 3️⃣ Fetch latest feature value
        value = (
            db.query(FeatureValue)
            .filter(
                FeatureValue.feature_id == feature.id,
                FeatureValue.entity_id == str(entity_id)
            )
            .order_by(FeatureValue.version.desc())
            .first()
        )

        if not value:
            raise HTTPException(
                status_code=404,
                detail=f"No value found for feature '{name}' and entity '{entity_id}'"
            )

        # 4️⃣ Cache & return
        FEATURE_CACHE[cache_key] = value.value
        feature_vector[name] = value.value

    return feature_vector
