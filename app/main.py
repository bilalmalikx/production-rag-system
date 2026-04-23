from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import upload, ask
from app.components.vector_store import VectorStoreComponent
from app.utils.config import config
import os

# Create FastAPI app
app = FastAPI(
    title="PDF QA System with LangGraph",
    description="Ask questions from your PDF documents using AI",
    version="1.0.0"
)

# Configure CORS for Angular (important!)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Angular default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router, prefix="/api", tags=["Upload"])
app.include_router(ask.router, prefix="/api", tags=["Ask"])

# Startup event: Load existing vector store if any
@app.on_event("startup")
async def startup_event():
    """Server start hote hi load karo existing vector store"""
    print("Starting PDF QA System...")
    
    # Ensure directories exist
    os.makedirs(config.UPLOAD_DIR, exist_ok=True)
    os.makedirs(config.VECTOR_STORE_PATH, exist_ok=True)
    
    # Load existing vector store
    vector_store = VectorStoreComponent()
    vector_store.load_vector_store()
    
    if vector_store.vector_store:
        print("✅ Loaded existing vector store")
    else:
        print("⚠️ No existing vector store found. Upload a PDF to get started.")
    
    print(f"🚀 Server ready at http://localhost:8000")
    print(f"📖 API docs at http://localhost:8000/docs")

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "PDF QA System API",
        "version": "1.0.0",
        "endpoints": {
            "upload": "POST /api/upload",
            "ask": "POST /api/ask",
            "docs": "/docs"
        }
    }

# Health check
@app.get("/health")
async def health():
    return {"status": "healthy", "service": "pdf-qa-backend"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)