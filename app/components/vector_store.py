from langchain_community.vectorstores import Chroma
from typing import List
from app.utils.config import config
from app.components.embeddings import EmbeddingsComponent
import os
import shutil
import json

class VectorStoreComponent:
    def __init__(self):
        self.embeddings_component = EmbeddingsComponent()
        self.persist_directory = config.VECTOR_STORE_PATH
        self.vector_store = None

        self.meta_file = os.path.join(self.persist_directory, "meta.json")

        # Ensure directory exists
        os.makedirs(self.persist_directory, exist_ok=True)

        # Auto-check embedding dimension
        self._check_and_reset_if_needed()

    # -------------------------------
    # Dimension safety check
    # -------------------------------
    def _check_and_reset_if_needed(self):
        current_dim = self.embeddings_component.dimension

        if os.path.exists(self.meta_file):
            try:
                with open(self.meta_file, "r") as f:
                    data = json.load(f)
                    saved_dim = data.get("dimension")

                if saved_dim != current_dim:
                    print("⚠️ Embedding dimension changed → resetting vector DB")
                    self.delete_vector_store()
            except Exception:
                # corrupted meta file fallback
                self.delete_vector_store()

        # Save current dimension
        with open(self.meta_file, "w") as f:
            json.dump({"dimension": current_dim}, f)

    # -------------------------------
    # Create vector store
    # -------------------------------
    def create_vector_store(self, documents: List):
        self.vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings_component.get_embeddings(),
            persist_directory=self.persist_directory
        )
        self.vector_store.persist()
        return self.vector_store

    # -------------------------------
    # Load existing store
    # -------------------------------
    def load_vector_store(self):
        if os.path.exists(self.persist_directory) and os.listdir(self.persist_directory):
            self.vector_store = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings_component.get_embeddings()
            )
        return self.vector_store

    # -------------------------------
    # Add new documents
    # -------------------------------
    def add_documents(self, documents: List):
        if self.vector_store is None:
            self.create_vector_store(documents)
        else:
            self.vector_store.add_documents(documents)
            self.vector_store.persist()

    # -------------------------------
    # Search
    # -------------------------------
    def similarity_search(self, query: str, k: int = 3) -> List:
        if self.vector_store is None:
            self.load_vector_store()

        if self.vector_store is None:
            return []

        return self.vector_store.similarity_search(query, k=k)

    # -------------------------------
    # Delete DB
    # -------------------------------
    def delete_vector_store(self):
        if os.path.exists(self.persist_directory):
            shutil.rmtree(self.persist_directory)

        os.makedirs(self.persist_directory, exist_ok=True)
        self.vector_store = None