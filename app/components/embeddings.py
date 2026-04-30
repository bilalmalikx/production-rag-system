# app/components/embeddings.py - FastEmbed version
from fastembed import TextEmbedding
from typing import List
from app.utils.config import config

class EmbeddingsComponent:
    def __init__(self):
        # Local model - no API key needed
        # Models available: "BAAI/bge-small-en-v1.5" (384 dimensions), "BAAI/bge-base-en" (768 dimensions)
        self.model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
        self.dimension = 384  # bge-small gives 384 dimensions
    
    def embed_query(self, text: str) -> List[float]:
        """Single text ka embedding"""
        embeddings = list(self.model.embed([text]))
        return embeddings[0].tolist()
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Multiple texts ka embeddings"""
        embeddings = list(self.model.embed(texts))
        return [emb.tolist() for emb in embeddings]
    
    def get_embeddings(self):
        """Return self for LangChain compatibility"""
        return self

    def __call__(self, texts):
        """LangChain ke liye callable interface"""
        if isinstance(texts, str):
            return self.embed_query(texts)
        return self.embed_documents(texts)