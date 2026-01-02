from app.database import engine, Base
from app.models.raw_table import RawTable
from app.models.feature import Feature
from app.models.feature_version import FeatureVersion
from app.models.feature_value import FeatureValue

Base.metadata.create_all(bind=engine)

print("✅ Database tables created successfully")
