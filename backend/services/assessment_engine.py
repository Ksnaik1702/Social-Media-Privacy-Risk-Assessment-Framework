"""
Unified Privacy Assessment Engine
Orchestrates the entire assessment pipeline:
Questionnaire Answers -> Feature Extraction -> Category Scoring ->
Overall Risk Scoring -> Findings Generation -> Recommendations -> Storage.
"""
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Optional

from backend.models.schemas import AssessmentResult, CategoryScoreDetail, FindingItem
from backend.services.questionnaire_data import CATEGORIES, QUESTIONS
from backend.services.feature_extractor import extract_privacy_features
from backend.services.scoring_engine import calculate_category_scores, calculate_overall_privacy_risk
from backend.services.findings_engine import generate_privacy_findings
from backend.services.recommendation_engine import generate_recommendations
from backend.database import save_assessment
from backend.config import classify_risk_level

DISCLAIMER_TEXT = (
    "This assessment is an educational cybersecurity risk framework based on self-reported "
    "configurations and behavioral indicators. It does NOT guarantee that an account will or "
    "will not be targeted or compromised, nor does it replace comprehensive organizational security audits."
)

def run_privacy_assessment(
    answers: Dict[str, str],
    custom_weights: Optional[Dict[str, float]] = None,
    save_to_db: bool = True
) -> Dict[str, Any]:
    """
    Executes the end-to-end privacy risk assessment pipeline.
    """
    assessment_id = f"priv_{uuid.uuid4().hex[:12]}"
    created_at = datetime.now(timezone.utc).isoformat()

    # Step 1: Feature Extraction
    features = extract_privacy_features(answers)

    # Step 2: Category Scoring
    category_scores_raw = calculate_category_scores(features)

    # Step 3: Overall Risk Scoring
    overall_score, risk_level = calculate_overall_privacy_risk(category_scores_raw, custom_weights)

    # Step 4: Findings Generation
    findings = generate_privacy_findings(answers, features)

    # Step 5: Recommendations Generation
    recommendations, priority_actions = generate_recommendations(findings)

    # Step 6: Format category details
    category_details = {}
    for cat_id, score in category_scores_raw.items():
        cat_meta = CATEGORIES.get(cat_id, {})
        category_details[cat_id] = {
            "category_id": cat_id,
            "category_name": cat_meta.get("name", cat_id),
            "score": score,
            "weight": custom_weights.get(cat_id, cat_meta.get("weight", 0.10)) if custom_weights else cat_meta.get("weight", 0.10),
            "risk_level": classify_risk_level(score),
            "max_score": 100.0
        }

    # Step 7: Persist Minimized Assessment (Privacy by Design)
    if save_to_db:
        save_assessment(
            assessment_id=assessment_id,
            overall_score=overall_score,
            risk_level=risk_level,
            category_scores=category_scores_raw,
            findings=findings,
            source_type="questionnaire"
        )

    return {
        "assessment_id": assessment_id,
        "created_at": created_at,
        "overall_score": overall_score,
        "risk_level": risk_level,
        "category_scores": category_details,
        "findings": findings,
        "recommendations": recommendations,
        "priority_actions": priority_actions,
        "total_questions_evaluated": len(QUESTIONS),
        "total_weaknesses_detected": len(findings),
        "disclaimer": DISCLAIMER_TEXT
    }
