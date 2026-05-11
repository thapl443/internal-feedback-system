from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float
from .database import Base
from datetime import datetime
import os

SCHEMA = os.getenv("DB_SCHEMA", "internal_portal")

class Announcement(Base):
    __tablename__ = "announcements"
    __table_args__ = {"schema": SCHEMA}
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class Complaint(Base):
    """ระบบกล่องรับเรื่อง + Decision Support"""
    __tablename__ = "complaints"
    __table_args__ = {"schema": SCHEMA}
    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String(200))
    description = Column(Text)
    # Automated classification and recommendation fields
    suggested_department = Column(String(100)) # Targeted department for resolution
    priority_score = Column(Integer)           # Heuristic priority score (1-5)
    ai_recommendation = Column(Text)           # System-generated resolution hint
    status = Column(String(50), default="Pending")
    created_at = Column(DateTime, default=datetime.utcnow)

class SportsScore(Base):
    """ตารางคะแนนกีฬาสี"""
    __tablename__ = "sports_scores"
    __table_args__ = {"schema": SCHEMA}
    id = Column(Integer, primary_key=True, index=True)
    team_color = Column(String(50)) # Red, Blue, Green, Yellow
    score = Column(Integer, default=0)
    last_updated = Column(DateTime, default=datetime.utcnow)

class SurveyResponse(Base):
    """แบบสอบถาม"""
    __tablename__ = "survey_responses"
    __table_args__ = {"schema": SCHEMA}
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String(200))
    answer = Column(String(50)) # Agree, Disagree, Neutral
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
