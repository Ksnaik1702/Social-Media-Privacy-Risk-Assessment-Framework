"""
Privacy Findings Engine
Scans feature vectors and answers to pinpoint detected privacy weaknesses.
Attaches severity levels, technical explanations, and remediation steps.
"""
from typing import Dict, List, Any
from backend.services.questionnaire_data import QUESTIONS, CATEGORIES

SEVERITY_ORDER = {
    "CRITICAL": 4,
    "HIGH": 3,
    "MEDIUM": 2,
    "LOW": 1
}

def generate_privacy_findings(
    answers: Dict[str, str],
    features: Dict[str, float]
) -> List[Dict[str, Any]]:
    """
    Identifies specific risk findings where user response indicates exposure.
    Only flags items exceeding the low-risk baseline (> 30.0).
    """
    findings = []

    for question in QUESTIONS:
        qid = question["id"]
        risk_val = features.get(qid, 0.0)

        # Flag as a finding if risk is meaningful (> 30 points)
        if risk_val >= 35.0:
            user_ans = answers.get(qid, "UNKNOWN")
            cat_id = question["category_id"]
            cat_name = CATEGORIES.get(cat_id, {}).get("name", cat_id)

            # Determine remediation priority based on severity
            severity = question.get("severity", "MEDIUM")
            if severity == "CRITICAL":
                priority = "IMMEDIATE"
            elif severity == "HIGH":
                priority = "IMPORTANT"
            else:
                priority = "GOOD_PRACTICE"

            findings.append({
                "id": f"find_{qid}",
                "question_id": qid,
                "category_id": cat_id,
                "category_name": cat_name,
                "severity": severity,
                "item": question["finding_title"],
                "user_answer": user_ans,
                "risk_contribution": risk_val,
                "explanation": question["explanation"],
                "recommendation": question["remediation"],
                "priority": priority
            })

    # Sort findings by severity descending, then by risk contribution descending
    findings.sort(
        key=lambda x: (SEVERITY_ORDER.get(x["severity"], 0), x["risk_contribution"]),
        reverse=True
    )

    return findings
