from fastapi import FastAPI
from app.api import raw, feature

app = FastAPI(title="Simple Feature Store")

app.include_router(raw.router)
app.include_router(feature.router)

@app.get("/")
def health():
    return {"status": "Feature Store is running"}