from langgraph.graph import StateGraph, END
from app.graph.state import GraphState, create_initial_state
from app.graph.nodes import (
    load_pdf_node,
    retrieve_chunks_node,
    agent_node,
    validate_node,
    error_node
)
from app.graph.edges import (
    should_continue_after_load,
    should_continue_after_retrieval,
    should_continue_after_agent,
    should_continue_after_validation
)

class PDFQAGraph:
    """
    LangGraph workflow — saare nodes aur edges ka compilation
    Ye graph decide karta hai ki flow kaise chalega
    """
    
    def __init__(self):
        self.graph = None
        self.build_graph()
    
    def build_graph(self):
        """Graph build karo — nodes aur edges add karo"""
        
        # Create new graph with state definition
        workflow = StateGraph(GraphState)
        
        # Add nodes
        workflow.add_node("load_pdf", load_pdf_node)
        workflow.add_node("retrieve", retrieve_chunks_node)
        workflow.add_node("agent", agent_node)
        workflow.add_node("validate", validate_node)
        workflow.add_node("error", error_node)
        
        # Set entry point — graph yahan se start hoga
        workflow.set_entry_point("load_pdf")
        
        # Add conditional edges
        workflow.add_conditional_edges(
            "load_pdf",
            should_continue_after_load,
            {
                "retrieve": "retrieve",
                "error": "error"
            }
        )
        
        workflow.add_conditional_edges(
            "retrieve",
            should_continue_after_retrieval,
            {
                "agent": "agent",
                "error": "error"
            }
        )
        
        workflow.add_conditional_edges(
            "agent",
            should_continue_after_agent,
            {
                "validate": "validate",
                "error": "error"
            }
        )
        
        workflow.add_conditional_edges(
            "validate",
            should_continue_after_validation,
            {
                "retrieve": "retrieve",  # Retry possible
                "end": END,
                "error": "error"
            }
        )
        
        # Error node goes to END
        workflow.add_edge("error", END)
        
        # Compile the graph
        self.graph = workflow.compile()
        print("✅ LangGraph workflow compiled successfully")
    
    def run(self, pdf_path: str = None, question: str = None, pdf_name: str = None) -> dict:
        """
        Graph execute karo — PDF processing se lekar answer tak
        """
        # Create initial state
        initial_state = create_initial_state()
        initial_state.update({
            "pdf_path": pdf_path,
            "question": question,
            "pdf_name": pdf_name,
            "start_time": None  # Time tracking optional
        })
        
        # Run the graph
        try:
            final_state = self.graph.invoke(initial_state)
            
            return {
                "success": final_state.get("status") != "failed",
                "answer": final_state.get("validated_answer", "No answer generated"),
                "confidence": final_state.get("confidence", 0),
                "sources": final_state.get("sources", []),
                "agent_used": final_state.get("agent_used"),
                "iterations": final_state.get("iteration_count", 0),
                "error": final_state.get("error")
            }
        except Exception as e:
            return {
                "success": False,
                "answer": f"Graph execution failed: {str(e)}",
                "confidence": 0,
                "sources": [],
                "error": str(e)
            }
    
    def get_graph_visualization(self):
        """
        Graph ka visualization return karta hai (debugging ke liye)
        Mermaid format mein
        """
        if self.graph:
            return self.graph.get_graph().draw_mermaid()
        return "Graph not compiled"

# Singleton instance
_pdf_qa_graph = None

def get_graph():
    """Global graph instance — har jagah same instance use karo"""
    global _pdf_qa_graph
    if _pdf_qa_graph is None:
        _pdf_qa_graph = PDFQAGraph()
    return _pdf_qa_graph