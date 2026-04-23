from typing import TypedDict, List, Dict, Any, Optional
from enum import Enum

class ProcessingStatus(Enum):
    """Graph processing ke states"""
    IDLE = "idle"
    LOADING = "loading"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class GraphState(TypedDict):
    """
    LangGraph ka State — har node ke beech mein ye data pass hoga
    Immutable nahi hai, nodes isko modify kar sakte hain
    """
    # Input
    pdf_path: Optional[str]
    question: Optional[str]
    pdf_name: Optional[str]
    
    # Processing
    pages: Optional[List[Any]]
    chunks: Optional[List[Any]]
    embeddings: Optional[List[Any]]
    vector_store: Optional[Any]
    
    # Retrieval
    retrieved_chunks: Optional[List[Dict[str, Any]]]
    context: Optional[str]
    
    # Answer generation
    prompt: Optional[str]
    raw_answer: Optional[str]
    
    # Validation
    validated_answer: Optional[str]
    confidence: Optional[float]
    sources: Optional[List[Dict[str, Any]]]
    
    # Agent decisions
    agent_decisions: Optional[List[Dict[str, Any]]]
    agent_used: Optional[str]
    
    # Status & Error
    status: str
    error: Optional[str]
    
    # Metadata
    iteration_count: int
    start_time: Optional[float]
    end_time: Optional[float]

def create_initial_state() -> GraphState:
    """Naya state create karta hai with default values"""
    return {
        "pdf_path": None,
        "question": None,
        "pdf_name": None,
        "pages": None,
        "chunks": None,
        "embeddings": None,
        "vector_store": None,
        "retrieved_chunks": None,
        "context": None,
        "prompt": None,
        "raw_answer": None,
        "validated_answer": None,
        "confidence": None,
        "sources": None,
        "agent_decisions": None,
        "agent_used": None,
        "status": ProcessingStatus.IDLE.value,
        "error": None,
        "iteration_count": 0,
        "start_time": None,
        "end_time": None
    }