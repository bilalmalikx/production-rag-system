from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """
    Sab agents ka base class
    Har agent ko decide karna hai ki kaunsa action lena hai
    """
    
    def __init__(self, name: str):
        self.name = name
        self.history = []  # Agent ke decisions ka record
    
    @abstractmethod
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Har agent ko ye method implement karna hoga
        Input: State ya user query
        Output: Decision + Action result
        """
        pass
    
    def log_decision(self, decision: str, reason: str):
        """Agent ke decision ko log karta hai (debugging ke liye)"""
        self.history.append({
            "agent": self.name,
            "decision": decision,
            "reason": reason,
            "timestamp": None  # Future mein datetime add kar sakte ho
        })
    
    def get_history(self) -> list:
        """Agent ka decision history return karta hai"""
        return self.history