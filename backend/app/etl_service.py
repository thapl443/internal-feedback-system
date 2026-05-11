from sqlalchemy.orm import Session
from .models import Complaint, SportsScore, Announcement, SurveyResponse
from .ai_service import AIInferenceService
import random

class InternalPortalService:
    @staticmethod
    def seed_data(db: Session):
        """Seed initial data if empty."""
        if db.query(SportsScore).count() == 0:
            for color in ["Red", "Blue", "Green", "Yellow"]:
                db.add(SportsScore(team_color=color, score=random.randint(50, 200)))
        
        if db.query(Announcement).count() == 0:
            db.add(Announcement(title="ยินดีต้อนรับสู่ Nexus Internal Portal", content="พอร์ทัลใหม่สำหรับพนักงานทุกคน"))
            db.add(Announcement(title="แจ้งปิดปรับปรุงระบบไฟ", content="วันเสาร์นี้เวลา 09:00 - 12:00 น."))
            
        db.commit()

    @staticmethod
    def analyze_complaint(complaint: Complaint):
        """
        Orchestrates the analysis of complaint content using the AI Inference Service.
        Demonstrates a professional service-oriented architecture.
        """
        # Call the dedicated AI service for text analysis
        analysis = AIInferenceService.analyze_text(complaint.subject, complaint.description)
        
        # Mapping structured output to DB model
        complaint.suggested_department = analysis.suggested_department
        complaint.priority_score = analysis.priority_score
        complaint.ai_recommendation = analysis.ai_recommendation
        complaint.sentiment = analysis.sentiment

        return complaint
