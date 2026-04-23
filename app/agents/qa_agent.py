from typing import Dict, Any, Optional
from app.agents.base_agent import BaseAgent
from app.agents.tools import (
    vector_search_tool, 
    answer_generation_tool, 
    confidence_check_tool,
    fallback_search_tool
)

class QAAgent(BaseAgent):
    """
    QA Agent: PDF se answer dhundhne aur generate karne ka specialist
    Decisions:
    1. Search karna hai ya nahi
    2. Kitne chunks retrieve karne hain
    3. Confidence low hai to fallback use karna hai ya nahi
    """
    
    def __init__(self):
        super().__init__(name="QAAgent")
        self.max_retries = 2
        self.confidence_threshold = 0.6
    
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Input: {"question": "what is scrum?", "pdf_name": "scrum.pdf"}
        Output: {"answer": "...", "confidence": 0.8, "sources": [...]}
        """
        question = input_data.get("question")
        pdf_name = input_data.get("pdf_name")
        
        if not question:
            return {
                "success": False,
                "answer": "No question provided",
                "confidence": 0.0,
                "sources": []
            }
        
        # Step 1: Search for relevant chunks
        self.log_decision("SEARCH", f"Searching for: {question[:50]}...")
        search_result = vector_search_tool(question, pdf_name)
        
        if not search_result["success"] or search_result["count"] == 0:
            self.log_decision("FALLBACK", "No chunks found, using fallback")
            fallback_result = fallback_search_tool(question)
            return {
                "success": fallback_result["success"],
                "answer": fallback_result.get("answer", "No information found"),
                "confidence": 0.1,
                "sources": []
            }
        
        chunks = search_result["chunks"]
        
        # Step 2: Generate answer from chunks
        self.log_decision("GENERATE", f"Generating answer from {len(chunks)} chunks")
        answer_result = answer_generation_tool(question, chunks)
        
        if not answer_result["success"]:
            return {
                "success": False,
                "answer": answer_result["message"],
                "confidence": 0.0,
                "sources": chunks[:2]
            }
        
        answer = answer_result["answer"]
        
        # Step 3: Check confidence
        confidence_result = confidence_check_tool(answer, chunks)
        
        if not confidence_result["is_valid"] and self.max_retries > 0:
            self.log_decision("RETRY", f"Low confidence, retrying with different strategy")
            # Retry with different prompt (future enhancement)
            self.max_retries -= 1
        
        # Step 4: Prepare sources for citation
        sources = []
        for chunk in chunks[:3]:  # Top 3 sources
            sources.append({
                "content": chunk["content"][:300] + "..." if len(chunk["content"]) > 300 else chunk["content"],
                "pdf_name": chunk["metadata"].get("pdf_name", "unknown"),
                "page": chunk["metadata"].get("page", 0)
            })
        
        return {
            "success": True,
            "answer": confidence_result["validated_answer"],
            "confidence": confidence_result["confidence"],
            "sources": sources,
            "agent_decisions": self.get_history()[-3:]  # Last 3 decisions
        }
    
    def should_delegate(self, question: str) -> bool:
        """
        Decide if this question should be delegated to another agent
        Agar question PDF-specific nahi hai to supervisor ko batana
        """
        # Simple rule: agar question mein "PDF", "document", "file" nahi hai
        # aur question general knowledge jaisa hai to delegate
        pdf_keywords = ["pdf", "document", "file", "upload", "scrum guide"]
        
        question_lower = question.lower()
        for keyword in pdf_keywords:
            if keyword in question_lower:
                return False  # PDF specific, handle myself
        
        # Agar question bahut short hai (less than 5 words)
        if len(question.split()) < 5:
            return False  # Probably simple question
        
        return True  # Delegate to supervisor