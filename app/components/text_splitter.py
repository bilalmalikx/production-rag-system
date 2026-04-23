from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List
from app.utils.config import config

class TextSplitterComponent:
    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def split_documents(self, documents: List) -> List:
        """
        Documents (pages) ko chote chunks mein todta hai
        Har chunk approximately chunk_size characters ka
        """
        chunks = self.splitter.split_documents(documents)
        
        # Har chunk mein page number add karo metadata mein
        for i, chunk in enumerate(chunks):
            chunk.metadata["chunk_id"] = i
        
        return chunks
    
    def split_text(self, text: str) -> List[str]:
        """Sirf text (bina metadata ke) chunks mein todna ho to"""
        return self.splitter.split_text(text)