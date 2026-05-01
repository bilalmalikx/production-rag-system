from typing import List
from app.utils.config import config
from openai import OpenAI

class EmbeddingsComponent:
    def __init__(self):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.model = "text-embedding-3-small"  # fast + cheap
        self.dimension = 1536  # OpenAI embedding size

    def embed_query(self, text: str) -> List[float]:
        response = self.client.embeddings.create(
            model=self.model,
            input=text
        )
        return response.data[0].embedding

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        response = self.client.embeddings.create(
            model=self.model,
            input=texts
        )
        return [item.embedding for item in response.data]

    def get_embeddings(self):
        return self

    def __call__(self, texts):
        if isinstance(texts, str):
            return self.embed_query(texts)
        return self.embed_documents(texts)