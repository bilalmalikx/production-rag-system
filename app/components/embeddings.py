from langchain_openai import OpenAIEmbeddings
from app.utils.config import config
from typing import List

class EmbeddingsComponent:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            model=config.EMBEDDING_MODEL,
            openai_api_key=config.OPENAI_API_KEY
        )
    
    def get_embeddings(self):
        """Embeddings object return karta hai (vector store ke liye)"""
        return self.embeddings
    
    def embed_text(self, text: str) -> List[float]:
        """Ek single text ka vector bana deta hai (1536 dimensions ka)"""
        return self.embeddings.embed_query(text)
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Multiple texts ka ek saath vector bana deta hai"""
        return self.embeddings.embed_documents(texts)