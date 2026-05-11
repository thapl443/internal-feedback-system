import os
from typing import Dict
from pydantic import BaseModel, Field

class AnalysisResult(BaseModel):
    suggested_department: str = Field(description="Department responsible for this issue")
    priority_score: int = Field(ge=1, le=5, description="Priority level from 1 to 5")
    ai_recommendation: str = Field(description="Actionable advice for the staff")
    sentiment: str = Field(description="Overall sentiment: Positive, Neutral, or Negative")

class AIInferenceService:
    """
    Service layer for AI Model Interaction.
    Architected to support both rule-based heuristics and external LLM APIs (OpenAI/Anthropic).
    """
    
    @staticmethod
    def get_system_prompt():
        return """
        You are an expert HR and Operations Assistant. 
        Analyze employee feedback and return a JSON object with:
        - suggested_department: (IT Support, HR, Facilities, General Admin)
        - priority_score: (1-5)
        - ai_recommendation: (Short actionable advice)
        - sentiment: (Positive, Neutral, Negative)
        Return ONLY valid JSON.
        """

    @classmethod
    def analyze_text(cls, subject: str, description: str) -> AnalysisResult:
        """
        High-level abstraction for text analysis.
        In a production environment, this would handle prompt templating and LLM orchestration.
        """
        # Toggle via .env for local vs production LLM usage
        use_real_api = os.getenv("USE_AI_API", "false").lower() == "true"
        
        full_text = f"Subject: {subject}\nDescription: {description}"
        
        if use_real_api:
            # Placeholder for actual LLM integration (e.g., via OpenAI SDK or httpx)
            # For demo purposes, we always route to the deterministic classification engine
            return cls._run_deterministic_inference(full_text)
        else:
            return cls._run_deterministic_inference(full_text)

    @staticmethod
    def _run_deterministic_inference(text: str) -> AnalysisResult:
        """
        A rule-based classification engine that mimics LLM outputs.
        Ensures consistent behavior for demonstration while maintaining the LLM interface.
        """
        text = text.lower()
        
        # Default state
        result = {
            "suggested_department": "General Admin",
            "priority_score": 1,
            "ai_recommendation": "Assign to department head for initial screening.",
            "sentiment": "Neutral"
        }

        # Heuristic matching
        if any(w in text for w in ["computer", "password", "internet", "wifi", "login", "คอม", "เน็ต", "รหัส"]):
            result.update({
                "suggested_department": "IT Support",
                "priority_score": 4,
                "ai_recommendation": "Identify hardware serial number and verify last maintenance log.",
                "sentiment": "Negative"
            })
        elif any(w in text for w in ["salary", "bonus", "leave", "เงิน", "สวัสดิการ", "ลา"]):
            result.update({
                "suggested_department": "HR",
                "priority_score": 3,
                "ai_recommendation": "Coordinate with payroll and update employee benefits portal.",
                "sentiment": "Neutral"
            })
        elif any(w in text for w in ["air", "light", "cleaning", "แอร์", "ไฟ", "สะอาด"]):
            result.update({
                "suggested_department": "Facilities",
                "priority_score": 2,
                "ai_recommendation": "Dispatch maintenance team to the reported location within 24 hours.",
                "sentiment": "Negative"
            })
            
        return AnalysisResult(**result)
