from sqlalchemy.orm import Session
from .models import Complaint, SportsScore, Announcement, SurveyResponse
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
        Heuristic-based decision support logic for automated routing.
        Analyzes subject and description to suggest department and priority.
        """
        text = (complaint.subject + " " + complaint.description).lower()
        
        # Rule-based classification engine logic
        if any(word in text for word in ["คอมพิวเตอร์", "รหัสผ่าน", "เน็ต", "wifi", "internet"]):
            complaint.suggested_department = "IT Support"
            complaint.priority_score = 4
            complaint.ai_recommendation = "ตรวจสอบประวัติการแจ้งซ่อมอุปกรณ์ และรีเซ็ตรหัสผ่านเบื้องต้น"
        elif any(word in text for word in ["เงินเดือน", "สวัสดิการ", "ลางาน", "วันหยุด"]):
            complaint.suggested_department = "HR"
            complaint.priority_score = 3
            complaint.ai_recommendation = "ตรวจสอบระเบียบการลาในคู่มือพนักงาน และประสานงานฝ่ายบัญชี"
        elif any(word in text for word in ["แอร์", "ไฟ", "ความสะอาด", "ที่จอดรถ"]):
            complaint.suggested_department = "Facilities"
            complaint.priority_score = 2
            complaint.ai_recommendation = "ส่งทีมช่างเข้าไปตรวจสอบพื้นที่ภายใน 24 ชม."
        else:
            complaint.suggested_department = "General Admin"
            complaint.priority_score = 1
            complaint.ai_recommendation = "ส่งเรื่องให้หัวหน้าแผนกตรวจสอบข้อมูลเพิ่มเติม"

        return complaint
