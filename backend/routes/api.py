"""
REST API Router
Exposes endpoints for:
- Assessment execution & retrieval
- Improvement simulation
- Privacy checklist & guidelines
- JSON profile/post feed analysis
- Safe local EXIF metadata inspection & stripping
- Dashboard aggregate telemetry
"""
import json
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException, UploadFile, File, Response
from fastapi.responses import JSONResponse

from backend.models.schemas import (
    QuestionnaireSubmission,
    ImprovementSimulationRequest,
    JsonProfilePayload
)
from backend.services.questionnaire_data import get_all_questions, get_categories
from backend.services.assessment_engine import run_privacy_assessment
from backend.services.improvement_simulator import simulate_improvements
from backend.services.json_file_analyzer import analyze_json_profile
from backend.services.exif_analyzer import inspect_image_metadata, strip_image_metadata
from backend.database import (
    get_assessment_by_id,
    delete_assessment_by_id,
    get_dashboard_statistics
)

router = APIRouter(prefix="/api", tags=["Privacy Risk Assessment"])

@router.get("/questions")
def get_questionnaire():
    """Returns the full 45-question diagnostic across all 10 security categories."""
    return {
        "categories": get_categories(),
        "questions": get_all_questions()
    }

@router.post("/assessment")
def submit_assessment(submission: QuestionnaireSubmission):
    """
    Evaluates questionnaire answers and generates comprehensive risk scoring,
    detected findings, and prioritized recommendations.
    """
    if not submission.answers:
        raise HTTPException(status_code=400, detail="Assessment answers cannot be empty.")
        
    result = run_privacy_assessment(
        answers=submission.answers,
        custom_weights=submission.custom_weights,
        save_to_db=True
    )
    return result

@router.get("/assessment/{assessment_id}")
def fetch_assessment(assessment_id: str):
    """Fetches a saved assessment by its anonymized ID."""
    record = get_assessment_by_id(assessment_id)
    if not record:
        raise HTTPException(status_code=404, detail="Assessment record not found.")
    return record

@router.get("/assessment/{assessment_id}/recommendations")
def fetch_recommendations(assessment_id: str):
    """Retrieves specific security recommendations for an assessment."""
    record = get_assessment_by_id(assessment_id)
    if not record:
        raise HTTPException(status_code=404, detail="Assessment record not found.")
    
    # Generate recommendations from findings
    findings = record.get("findings", [])
    from backend.services.recommendation_engine import generate_recommendations
    recs, actions = generate_recommendations(findings)
    return {
        "assessment_id": assessment_id,
        "recommendations": recs,
        "priority_actions": actions
    }

@router.post("/assessment/simulate-improvement")
def simulate_improvement_endpoint(req: ImprovementSimulationRequest):
    """
    Interactive 'What-If' simulator: calculates risk reduction score
    and demonstrates the defensive power of hardening privacy settings.
    """
    res = simulate_improvements(
        original_answers=req.original_answers,
        simulated_changes=req.simulated_changes
    )
    return res

@router.delete("/assessment/{assessment_id}")
def delete_assessment(assessment_id: str):
    """Supports Right to Erasure / GDPR data minimization by deleting an assessment."""
    deleted = delete_assessment_by_id(assessment_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Assessment ID not found or already deleted.")
    return {"message": "Assessment permanently erased.", "assessment_id": assessment_id}

@router.get("/dashboard/stats")
def dashboard_stats():
    """Provides aggregate statistics and telemetry across completed assessments."""
    return get_dashboard_statistics()

@router.get("/privacy-checklist")
def privacy_checklist():
    """Provides an actionable, printable social media privacy checklist."""
    return {
        "title": "Comprehensive Social Media Privacy & Security Checklist",
        "description": "Essential defensive actions to harden your digital footprint across social platforms.",
        "checklist": [
            {"id": "c1", "cat": "Profile", "action": "Switch profile to Private or Friends-only where feasible."},
            {"id": "c2", "cat": "Profile", "action": "Turn off search engine indexation (Google/Bing indexing)."},
            {"id": "c3", "cat": "PII", "action": "Remove phone numbers and personal email addresses from bios and public fields."},
            {"id": "c4", "cat": "PII", "action": "Hide full birth year; limit birthday visibility to 'Only Me'."},
            {"id": "c5", "cat": "Location", "action": "Disable real-time location check-ins and live event tagging."},
            {"id": "c6", "cat": "Location", "action": "Never post vacation or travel itineraries until you have returned home."},
            {"id": "c7", "cat": "Location", "action": "Turn off camera GPS geotagging permissions on mobile devices."},
            {"id": "c8", "cat": "Content", "action": "Never post photos showing employee badges, building floor numbers, or computer monitors."},
            {"id": "c9", "cat": "Content", "action": "Blur or omit minors, school uniforms, and identifiable crests from public media."},
            {"id": "c10", "cat": "Tagging", "action": "Enable Timeline / Tag Review to approve tags before they appear on your profile."},
            {"id": "c11", "cat": "Connections", "action": "Strictly reject or verify connection requests from unfamiliar profiles."},
            {"id": "c12", "cat": "Security", "action": "Enable Multi-Factor Authentication (MFA) via authenticator app or hardware token."},
            {"id": "c13", "cat": "Security", "action": "Deploy a password manager; never reuse master passwords across accounts."},
            {"id": "c14", "cat": "Security", "action": "Enable unrecognized login alerts via push notification and email."},
            {"id": "c15", "cat": "Third-Party", "action": "Audit connected third-party OAuth apps quarterly; revoke unused game or quiz tokens."},
            {"id": "c16", "cat": "Social Engineering", "action": "Never disclose OTP verification codes to anyone over chat or phone."},
            {"id": "c17", "cat": "Footprint", "action": "Archive or purge old historical posts older than 12-24 months."},
            {"id": "c18", "cat": "Footprint", "action": "Identify and permanently delete abandoned legacy accounts (Tumblr, Ask.fm, etc.)."}
        ]
    }

@router.post("/analyze-json")
def analyze_json_endpoint(payload: JsonProfilePayload):
    """
    Analyzes imported synthetic profile.json and posts.json without web scraping.
    """
    return analyze_json_profile(payload.profile, payload.posts)

@router.post("/metadata/inspect")
async def inspect_metadata_endpoint(file: UploadFile = File(...)):
    """
    Safely inspects EXIF metadata of an uploaded photo entirely in-memory.
    Never persists the image to permanent disk.
    """
    content = await file.read()
    res = inspect_image_metadata(content, filename=file.filename or "uploaded_photo.jpg")
    return res

@router.post("/metadata/strip")
async def strip_metadata_endpoint(file: UploadFile = File(...)):
    """
    Safely strips EXIF and GPS metadata from an image in-memory
    and returns the sanitized, clean image bytes.
    """
    content = await file.read()
    clean_bytes = strip_image_metadata(content)
    media_type = file.content_type or "image/jpeg"
    return Response(
        content=clean_bytes,
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename=cleaned_{file.filename or 'photo.jpg'}"}
    )
