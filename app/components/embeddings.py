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
        """Returns embeddings object (for vector store)"""
        return self.embeddings
    
    def embed_text(self, text: str) -> List[float]:
        """Generates embedding for a single text"""
        return self.embeddings.embed_query(text)
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Generates embeddings for multiple texts"""
        return self.embeddings.embed_documents(texts)