from typing import List, Dict, Any, Optional
from app.services.retrieval_service import RetrievalService
from app.services.qa_service import QAService

# Global service instances (lazy loading)
_retrieval_service = None
_qa_service = None

def get_retrieval_service():
    """Singleton pattern — ek hi instance reuse karo"""
    global _retrieval_service
    if _retrieval_service is None:
        _retrieval_service = RetrievalService()
    return _retrieval_service

def get_qa_service():
    """Singleton pattern — ek hi instance reuse karo"""
    global _qa_service
    if _qa_service is None:
        _qa_service = QAService()
    return _qa_service

def vector_search_tool(query: str, pdf_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Tool 1: PDF mein search karo
    Agent ye tool use karega relevant chunks dhondhne ke liye
    """
    retrieval_service = get_retrieval_service()
    
    try:
        chunks = retrieval_service.retrieve_relevant_chunks(query, pdf_name)
        
        if not chunks:
            return {
                "success": False,
                "message": "No relevant information found",
                "chunks": [],
                "count": 0
            }
        
        return {
            "success": True,
            "message": f"Found {len(chunks)} relevant chunks",
            "chunks": chunks,
            "count": len(chunks)
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Search failed: {str(e)}",
            "chunks": [],
            "count": 0
        }

def answer_generation_tool(question: str, context_chunks: List[Dict]) -> Dict[str, Any]:
    """
    Tool 2: Chunks se answer generate karo
    Agent ye tool use karega final answer banane ke liye
    """
    qa_service = get_qa_service()
    
    try:
        # Context format karo
        retrieval_service = get_retrieval_service()
        context = retrieval_service.format_context(context_chunks)
        
        # Answer generate karo
        from app.components.llm import LLMComponent
        llm = LLMComponent()
        answer = llm.generate_with_context(question, context)
        
        return {
            "success": True,
            "answer": answer,
            "message": "Answer generated successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "answer": None,
            "message": f"Answer generation failed: {str(e)}"
        }

def confidence_check_tool(answer: str, chunks: List[Dict]) -> Dict[str, Any]:
    """
    Tool 3: Answer ki confidence check karo
    Agent ye tool use karega decide karne ke liye ki answer sahi hai ya nahi
    """
    from app.services.guardrails_service import GuardrailsService
    guardrails = GuardrailsService()
    
    context = " ".join([c.get("content", "") for c in chunks]) if chunks else ""
    
    is_valid, validated_answer = guardrails.validate_answer(answer, context)
    
    return {
        "success": True,
        "is_valid": is_valid,
        "validated_answer": validated_answer if not is_valid else answer,
        "confidence": 0.9 if is_valid else 0.3,
        "message": "Answer is grounded" if is_valid else "Potential hallucination detected"
    }

def fallback_search_tool(query: str) -> Dict[str, Any]:
    """
    Tool 4: Fallback search (future mein implement karna)
    Agar PDF mein answer nahi mila to web search etc
    """
    # TODO: Future mein implement karna (Google Search, Wikipedia, etc)
    return {
        "success": False,
        "message": "Fallback search not implemented yet",
        "answer": "I couldn't find this information in the document."
    }