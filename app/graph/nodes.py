from app.graph.state import GraphState, ProcessingStatus
from app.services.ingestion_service import IngestionService
from app.services.retrieval_service import RetrievalService
from app.agents.supervisor_agent import SupervisorAgent
from typing import Dict, Any
import time

# Initialize services (singleton pattern)
ingestion_service = IngestionService()
retrieval_service = RetrievalService()
supervisor_agent = SupervisorAgent()

def load_pdf_node(state: GraphState) -> Dict[str, Any]:
    """
    Node 1: PDF load karta hai aur chunks mein todta hai
    """
    print(f"[NODE] load_pdf_node - Processing: {state.get('pdf_path')}")
    
    if not state.get("pdf_path"):
        return {
            "status": ProcessingStatus.FAILED.value,
            "error": "No PDF path provided"
        }
    
    try:
        # Load and process PDF
        result = ingestion_service.process_pdf(
            state["pdf_path"], 
            state.get("pdf_name", "unknown.pdf")
        )
        
        if not result["success"]:
            return {
                "status": ProcessingStatus.FAILED.value,
                "error": result.get("error", "PDF processing failed")
            }
        
        return {
            "status": ProcessingStatus.PROCESSING.value,
            "pages": result.get("pages"),
            "chunks": result.get("chunks"),
            "iteration_count": state.get("iteration_count", 0) + 1
        }
        
    except Exception as e:
        return {
            "status": ProcessingStatus.FAILED.value,
            "error": f"PDF loading failed: {str(e)}"
        }

def retrieve_chunks_node(state: GraphState) -> Dict[str, Any]:
    """
    Node 2: Question ke relevant chunks retrieve karta hai
    """
    print(f"[NODE] retrieve_chunks_node - Question: {state.get('question')}")
    
    if not state.get("question"):
        return {
            "status": ProcessingStatus.FAILED.value,
            "error": "No question provided"
        }
    
    try:
        chunks = retrieval_service.retrieve_relevant_chunks(
            state["question"],
            state.get("pdf_name")
        )
        
        if not chunks:
            return {
                "retrieved_chunks": [],
                "context": "",
                "status": ProcessingStatus.PROCESSING.value
            }
        
        context = retrieval_service.format_context(chunks)
        
        return {
            "retrieved_chunks": chunks,
            "context": context,
            "status": ProcessingStatus.PROCESSING.value
        }
        
    except Exception as e:
        return {
            "status": ProcessingStatus.FAILED.value,
            "error": f"Retrieval failed: {str(e)}"
        }

def agent_node(state: GraphState) -> Dict[str, Any]:
    """
    Node 3: Supervisor Agent ko call karta hai
    Agent decide karega answer kaise generate karna hai
    """
    print(f"[NODE] agent_node - Calling Supervisor Agent")
    
    try:
        # Prepare input for agent
        agent_input = {
            "question": state.get("question"),
            "pdf_name": state.get("pdf_name"),
            "retrieved_chunks": state.get("retrieved_chunks")
        }
        
        # Run supervisor agent
        agent_result = supervisor_agent.run(agent_input)
        
        return {
            "raw_answer": agent_result.get("answer"),
            "confidence": agent_result.get("confidence", 0.5),
            "sources": agent_result.get("sources", []),
            "agent_decisions": agent_result.get("agent_decisions", []),
            "agent_used": agent_result.get("agent_used", "SupervisorAgent"),
            "status": ProcessingStatus.PROCESSING.value
        }
        
    except Exception as e:
        return {
            "status": ProcessingStatus.FAILED.value,
            "error": f"Agent execution failed: {str(e)}"
        }

def validate_node(state: GraphState) -> Dict[str, Any]:
    """
    Node 4: Answer validate karta hai (guardrails)
    """
    print(f"[NODE] validate_node - Validating answer")
    
    from app.services.guardrails_service import GuardrailsService
    guardrails = GuardrailsService()
    
    answer = state.get("raw_answer", "")
    chunks = state.get("retrieved_chunks", [])
    
    if not answer:
        return {
            "validated_answer": "No answer generated",
            "status": ProcessingStatus.FAILED.value,
            "error": "Empty answer from agent"
        }
    
    # Prepare context for validation
    context = " ".join([c.get("content", "") for c in chunks]) if chunks else ""
    
    # Validate
    is_valid, validated_answer = guardrails.validate_answer(answer, context)
    
    # Sanitize
    final_answer = guardrails.sanitize_answer(validated_answer)
    
    return {
        "validated_answer": final_answer,
        "status": ProcessingStatus.COMPLETED.value if is_valid else ProcessingStatus.PROCESSING.value,
        "confidence": 0.9 if is_valid else 0.3
    }

def error_node(state: GraphState) -> Dict[str, Any]:
    """
    Node 5: Error handler — koi node fail hoti hai to ye chalega
    """
    print(f"[NODE] error_node - Handling error: {state.get('error')}")
    
    return {
        "validated_answer": f"An error occurred: {state.get('error', 'Unknown error')}",
        "status": ProcessingStatus.FAILED.value,
        "end_time": time.time()
    }