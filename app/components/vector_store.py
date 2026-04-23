from langchain_community.vectorstores import Chroma
from typing import List, Optional
from app.utils.config import config
from app.components.embeddings import EmbeddingsComponent
import os
import shutil

class VectorStoreComponent:
    def __init__(self):
        self.embeddings_component = EmbeddingsComponent()
        self.persist_directory = config.VECTOR_STORE_PATH
        self.vector_store = None
        
        # Ensure directory exists
        os.makedirs(self.persist_directory, exist_ok=True)
    
    def create_vector_store(self, documents: List):
        """
        Naya vector store create karta hai documents se
        Chroma DB mein save bhi karta hai (persistent)
        """
        self.vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings_component.get_embeddings(),
            persist_directory=self.persist_directory
        )
        self.vector_store.persist()
        return self.vector_store
    
    def load_vector_store(self):
        """
        Previously saved vector store load karta hai
        (Jaise hi server start hoga, ye call karna)
        """
        if os.path.exists(self.persist_directory) and os.listdir(self.persist_directory):
            self.vector_store = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings_component.get_embeddings()
            )
        return self.vector_store
    
    def add_documents(self, documents: List):
        """Existing vector store mein naye documents add karna"""
        if self.vector_store is None:
            self.create_vector_store(documents)
        else:
            self.vector_store.add_documents(documents)
            self.vector_store.persist()
    
    def similarity_search(self, query: str, k: int = 3) -> List:
        """Question ke similar chunks find karta hai"""
        if self.vector_store is None:
            self.load_vector_store()
        
        if self.vector_store is None:
            return []
        
        results = self.vector_store.similarity_search(query, k=k)
        return results
    
    def delete_vector_store(self):
        """Purana vector store delete karna (reset ke liye)"""
        if os.path.exists(self.persist_directory):
            shutil.rmtree(self.persist_directory)
            os.makedirs(self.persist_directory, exist_ok=True)
        self.vector_store = None