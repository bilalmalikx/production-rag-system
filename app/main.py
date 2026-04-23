from fastapi import FastAPI
from app.api.routes import upload, ask

app = FastAPI(title="PDF QA System with LangGraph")

app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(ask.router, prefix="/api", tags=["ask"])

@app.get("/")
def root():
    return {"message": "PDF QA System is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
