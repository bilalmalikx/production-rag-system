from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from app.utils.config import config

class LLMComponent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=config.LLM_MODEL,
            temperature=0.3,  # Low temperature = more factual, less creative
            openai_api_key=config.OPENAI_API_KEY
        )
    
    def generate_response(self, prompt: str) -> str:
        """Raw prompt bhejo, answer lo"""
        response = self.llm.invoke(prompt)
        return response.content
    
    def generate_with_context(self, question: str, context: str) -> str:
        """Question + context dekar answer generate karo"""
        system_prompt = """You are a helpful assistant. Using the provided document context, answer the user's question.

GUIDELINES:
- If the question asks for "first step" or "steps", look for numbered items, bullet points, or sequential information.
- If exact answer not found, provide the MOST RELEVANT information you CAN find.
- If the context has related concepts, explain them.
- ONLY say "I don't know" if the context is completely empty.

Be helpful and extract value from whatever context is provided."""
        
        user_prompt = f"""Context:
        {context}
        
        Question: {question}
        
        Answer based only on the above context:"""
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
    
    def get_llm_instance(self):
        """Direct LLM instance return karta hai (advanced use cases ke liye)"""
        return self.llm