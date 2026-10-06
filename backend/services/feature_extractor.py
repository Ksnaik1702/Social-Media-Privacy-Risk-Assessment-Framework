"""
Privacy Feature Extraction Module
Extracts numerical risk features from questionnaire answers.
Transforms qualitative answers (YES/NO/PUBLIC/PRIVATE etc.) into standardized
risk values between 0.0 (safe/defensive) and 100.0 (high exposure/risk).
"""
from typing import Dict, Any
from backend.services.questionnaire_data import QUESTIONS, get_question_by_id

def extract_privacy_features(answers: Dict[str, str]) -> Dict[str, float]:
    """
    Extract numerical risk feature vector from user response dictionary.
    Returns: Dict[question_id, float risk score (0-100)]
    """
    feature_vector: Dict[str, float] = {}

    for question in QUESTIONS:
        qid = question["id"]
        user_answer = answers.get(qid, "").strip().upper()
        risk_map = question["risk_mapping"]

        if user_answer in risk_map:
            feature_vector[qid] = float(risk_map[user_answer])
        else:
            # Fallback handling if unanswered or invalid
            # Default to moderate risk if question was omitted or unsure
            feature_vector[qid] = float(risk_map.get("NOT_SURE", 50.0))

    return feature_vector
