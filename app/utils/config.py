import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # PDF Processing
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 500))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 50))
    
    # Paths
    VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "data/vector_store")
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "data/uploads")
    
    # Model names
    # EMBEDDING_MODEL = "text-embedding-ada-002"
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    LLM_MODEL = "gpt-3.5-turbo"
    
    # Retrieval
    TOP_K_RESULTS = 3

config = Config()