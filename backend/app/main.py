from fastapi import FastAPI, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import engine, get_db
from .models import Base, Announcement, Complaint, SportsScore, SurveyResponse
from .etl_service import InternalPortalService
from pydantic import BaseModel

import time
from datetime import datetime
from sqlalchemy.exc import OperationalError
from sqlalchemy import text
import os

# Initialize DB with Retry Logic to handle container startup race conditions
def init_db():
    retries = 5
    schema_name = os.getenv("DB_SCHEMA", "internal_portal")
    while retries > 0:
        try:
            # Ensure the custom schema exists before table creation
            with engine.connect() as conn:
                conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema_name}"))
                conn.commit()

            Base.metadata.create_all(bind=engine)
            print(f"Successfully connected and ensured schema '{schema_name}'")
            break
        except OperationalError:
            retries -= 1
            print(f"Waiting for database... ({retries} retries left)")
            time.sleep(2)

init_db()

app = FastAPI(title="Nexus Internal Portal API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Seed data on startup with retry logic
@app.on_event("startup")
def startup_event():
    retries = 5
    while retries > 0:
        try:
            db = next(get_db())
            InternalPortalService.seed_data(db)
            print("Successfully seeded initial data")
            break
        except Exception as e:
            retries -= 1
            print(f"Seeding failed, retrying... ({retries} left). Error: {e}")
            time.sleep(3)

class ComplaintCreate(BaseModel):
    subject: str
    description: str

class SurveyCreate(BaseModel):
    topic: str
    answer: str
    comment: str

@app.get("/announcements")
def get_announcements(db: Session = Depends(get_db)):
    return db.query(Announcement).order_by(Announcement.created_at.desc()).all()

@app.get("/scores")
def get_scores(db: Session = Depends(get_db)):
    return db.query(SportsScore).order_by(SportsScore.id).all()

@app.post("/complaints")
def create_complaint(data: ComplaintCreate, db: Session = Depends(get_db)):
    new_complaint = Complaint(subject=data.subject, description=data.description)
    # Automated analysis for department routing and priority
    analyzed = InternalPortalService.analyze_complaint(new_complaint)
    db.add(analyzed)
    db.commit()
    db.refresh(analyzed)
    return analyzed

@app.get("/complaints")
def get_complaints(db: Session = Depends(get_db)):
    return db.query(Complaint).order_by(Complaint.created_at.desc()).all()

@app.post("/surveys")
def create_survey(data: SurveyCreate, db: Session = Depends(get_db)):
    new_survey = SurveyResponse(**data.dict())
    db.add(new_survey)
    db.commit()
    return {"message": "Survey submitted"}
# Admin APIs
class AnnouncementCreate(BaseModel):
    title: str
    content: str

@app.post("/announcements")
def create_announcement(data: AnnouncementCreate, db: Session = Depends(get_db)):
    new_ann = Announcement(title=data.title, content=data.content)
    db.add(new_ann)
    db.commit()
    db.refresh(new_ann)
    return new_ann

@app.post("/etl/run")
def run_etl_manually(db: Session = Depends(get_db)):
    InternalPortalService.seed_data(db)
    return {"status": "success", "message": "ETL process triggered manually"}

@app.patch("/scores/{score_id}")
def update_score(score_id: int, score: int, db: Session = Depends(get_db)):
    team_score = db.query(SportsScore).filter(SportsScore.id == score_id).first()
    if team_score:
        team_score.score = score
        team_score.last_updated = datetime.now()
        db.commit()
    return team_score

@app.delete("/announcements/{ann_id}")
def delete_announcement(ann_id: int, db: Session = Depends(get_db)):
    ann = db.query(Announcement).filter(Announcement.id == ann_id).first()
    if ann:
        db.delete(ann)
        db.commit()
    return {"status": "deleted"}

@app.get("/admin/raw-db")
def get_raw_db(db: Session = Depends(get_db)):
    # Debugging endpoint for raw table state verification
    return {
        "announcements": db.query(Announcement).all(),
        "complaints": db.query(Complaint).all(),
        "sports_scores": db.query(SportsScore).order_by(SportsScore.id).all(),
        "surveys": db.query(SurveyResponse).all()
    }

@app.get("/analytics/summary")
def get_summary(db: Session = Depends(get_db)):
    """
    Aggregation logic for management reporting.
    """
    total_complaints = db.query(Complaint).count()
    dept_distribution = {}
    for c in db.query(Complaint).all():
        dept_distribution[c.suggested_department] = dept_distribution.get(c.suggested_department, 0) + 1
    
    return {
        "total_complaints": total_complaints,
        "department_load": dept_distribution,
        "active_announcements": db.query(Announcement).count()
    }
