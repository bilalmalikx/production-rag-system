from app.graph.state import GraphState, ProcessingStatus

def should_continue_after_load(state: GraphState) -> str:
    """
    Decision: PDF load hone ke baad kya karna hai?
    Returns: Next node name
    """
    if state.get("status") == ProcessingStatus.FAILED.value:
        return "error"
    
    if state.get("chunks"):
        return "retrieve"  # Chunks ready hain, retrieval pe jao
    else:
        return "error"  # Kuch galat hua

def should_continue_after_retrieval(state: GraphState) -> str:
    """
    Decision: Chunks retrieve hone ke baad?
    """
    if state.get("status") == ProcessingStatus.FAILED.value:
        return "error"
    
    chunks = state.get("retrieved_chunks", [])
    
    if chunks and len(chunks) > 0:
        return "agent"  # Chunks mile, agent pe jao
    else:
        # No chunks found — still try agent (it will handle fallback)
        return "agent"

def should_continue_after_agent(state: GraphState) -> str:
    """
    Decision: Agent ne answer generate kiya, ab validate karna hai?
    """
    if state.get("status") == ProcessingStatus.FAILED.value:
        return "error"
    
    if state.get("raw_answer"):
        return "validate"
    else:
        return "error"

def should_continue_after_validation(state: GraphState) -> str:
    """
    Decision: Validation ke baad? Done ya retry?
    """
    if state.get("status") == ProcessingStatus.FAILED.value:
        return "error"
    
    # Agar confidence bahut low hai aur retry kar sakte hain
    confidence = state.get("confidence", 0)
    iteration = state.get("iteration_count", 0)
    
    if confidence < 0.4 and iteration < 2:
        return "retrieve"  # Retry with different strategy
    else:
        return "end"

def route_based_on_question(state: GraphState) -> str:
    """
    Decision: Question ke type ke hisaab se different flow
    Future enhancement
    """
    question = state.get("question", "").lower()
    
    # Agar question summarization hai to special flow
    if any(word in question for word in ["summarize", "summary", "brief"]):
        return "summary_flow"  # Future node
    
    # Default flow
    return "standard_flow"