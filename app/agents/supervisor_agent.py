from typing import Dict, Any, Optional
from app.agents.base_agent import BaseAgent
from app.agents.qa_agent import QAAgent

class SupervisorAgent(BaseAgent):
    """
    Supervisor Agent: Decide karta hai kaun sa agent use karna hai
    Future mein multiple agents honge (SummarizationAgent, ComparisonAgent, etc)
    Abhi ke liye sirf QA agent hai
    """
    
    def __init__(self):
        super().__init__(name="SupervisorAgent")
        self.qa_agent = QAAgent()
        
        # Agent registry (future expansion)
        self.agents = {
            "qa": self.qa_agent,
            # "summary": SummarizationAgent(),  # Future
            # "compare": ComparisonAgent(),     # Future
        }
    
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Input: {"question": "...", "pdf_name": "..."}
        Output: Final answer after routing to appropriate agent
        """
        question = input_data.get("question")
        
        if not question:
            return {
                "success": False,
                "answer": "No question provided",
                "agent_used": None
            }
        
        # Step 1: Decide which agent to use
        selected_agent = self.route_question(question)
        
        self.log_decision(
            "ROUTE", 
            f"Routing to {selected_agent} agent for: {question[:50]}..."
        )
        
        # Step 2: Call the selected agent
        if selected_agent == "qa":
            result = self.qa_agent.run(input_data)
            result["agent_used"] = "QAAgent"
            return result
        else:
            # Fallback to QA agent if agent not found
            result = self.qa_agent.run(input_data)
            result["agent_used"] = "QAAgent (fallback)"
            return result
    
    def route_question(self, question: str) -> str:
        """
        Decide which agent should handle this question
        Rules-based routing (future: LLM-based routing)
        """
        question_lower = question.lower()
        
        # Rule 1: Summarization requests
        if any(word in question_lower for word in ["summarize", "summary", "brief", "overview"]):
            # Future: return "summary"
            return "qa"  # Abhi ke liye QA agent handle karega
        
        # Rule 2: Comparison requests
        if any(word in question_lower for word in ["compare", "difference", "versus", "vs"]):
            # Future: return "compare"
            return "qa"
        
        # Rule 3: Default to QA agent
        return "qa"
    
    def add_agent(self, name: str, agent: BaseAgent):
        """Dynamically naye agents add karne ke liye (runtime mein)"""
        self.agents[name] = agent
        self.log_decision("ADD_AGENT", f"Added new agent: {name}")
    
    def get_agent_status(self) -> Dict[str, str]:
        """Sab agents ka status check karna"""
        status = {}
        for name, agent in self.agents.items():
            status[name] = "available"
        return status