from app.services.feature_compute import compute_feature
from app.models.feature_version import FeatureVersion
from app.models.feature_value import FeatureValue

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

    # 2️⃣ Determine new version
    new_version = 1 if not latest else latest.version + 1

    # 3️⃣ Store version metadata
    feature_version = FeatureVersion(
        feature_id=feature.id,
        version=new_version,
        logic=logic
    )
    db.add(feature_version)
    db.commit()

    # 4️⃣ Compute feature values
    values = compute_feature(raw_table, logic)

    # 5️⃣ Store feature values
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

    return new_version
