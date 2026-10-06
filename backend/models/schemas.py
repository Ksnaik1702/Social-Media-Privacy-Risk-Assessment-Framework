"""
Data Contracts and Pydantic Models for Privacy Risk Assessment
Strictly designed according to Privacy by Design:
- NO actual phone numbers, passwords, emails, exact home addresses, or private messages.
- ONLY privacy configuration responses and self-reported risk behaviors.
"""
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class QuestionnaireSubmission(BaseModel):
    """
    Submissions from the 40+ Question Assessment.
    Key is question_id (e.g. 'q_pv_1'), Value is string answer.
    """
    answers: Dict[str, str] = Field(
        ..., 
        description="Map of question_id to answer string (YES, NO, SOMETIMES, NOT_SURE, PUBLIC, FRIENDS, PRIVATE)"
    )
    custom_weights: Optional[Dict[str, float]] = Field(
        None,
        description="Optional custom category weights totaling 1.0"
    )

class ImprovementSimulationRequest(BaseModel):
    """
    Simulated changes to test risk reduction.
    """
    original_answers: Dict[str, str]
    simulated_changes: Dict[str, str] = Field(
        ...,
        description="Map of question_ids to the improved answers (e.g. {'q_sec_1': 'YES', 'q_pi_1': 'NO'})"
    )

class CategoryScoreDetail(BaseModel):
    category_id: str
    category_name: str
    score: float
    weight: float
    risk_level: str
    max_score: float = 100.0

class FindingItem(BaseModel):
    id: str
    category_id: str
    category_name: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    item: str
    explanation: str
    recommendation: str
    priority: str  # IMMEDIATE, IMPORTANT, GOOD_PRACTICE

class AssessmentResult(BaseModel):
    assessment_id: str
    created_at: str
    overall_score: float
    risk_level: str
    category_scores: Dict[str, CategoryScoreDetail]
    findings: List[FindingItem]
    recommendations: List[Dict[str, Any]]
    priority_actions: List[str]
    disclaimer: str

class SimulationResult(BaseModel):
    original_score: float
    original_risk_level: str
    simulated_score: float
    simulated_risk_level: str
    risk_reduction_points: float
    risk_reduction_percent: float
    category_comparison: Dict[str, Dict[str, float]]
    resolved_findings: List[str]
    disclaimer: str

class JsonProfilePayload(BaseModel):
    """
    Safe file ingestion schema for exported or synthetic social profiles.
    """
    profile: Dict[str, Any]
    posts: List[Dict[str, Any]] = []

class DashboardStats(BaseModel):
    total_assessments: int
    average_score: float
    risk_distribution: Dict[str, int]
    top_weaknesses: List[Dict[str, Any]]
    recent_assessments: List[Dict[str, Any]]
