"""
Privacy Risk Scoring Engine
Calculates:
1. Category-Wise Privacy Risk Scores (0 - 100)
2. Overall Privacy Risk Score (0 - 100) using weighted aggregation
3. Risk Level Classification (LOW, MODERATE, HIGH, CRITICAL)

Higher Score = HIGHER Exposure / Risk.
0-20   = LOW
21-40  = MODERATE
41-70  = HIGH
71-100 = CRITICAL
"""
from typing import Dict, Tuple, Optional
from backend.config import DEFAULT_CATEGORY_WEIGHTS, classify_risk_level
from backend.services.questionnaire_data import CATEGORIES, QUESTIONS

def calculate_category_scores(features: Dict[str, float]) -> Dict[str, float]:
    """
    Groups question features by category and calculates the average risk score (0-100) for each.
    """
    category_totals: Dict[str, float] = {cat: 0.0 for cat in CATEGORIES}
    category_counts: Dict[str, int] = {cat: 0 for cat in CATEGORIES}

    for question in QUESTIONS:
        qid = question["id"]
        cat_id = question["category_id"]
        if qid in features and cat_id in category_totals:
            category_totals[cat_id] += features[qid]
            category_counts[cat_id] += 1

    category_scores: Dict[str, float] = {}
    for cat_id in CATEGORIES:
        count = category_counts[cat_id]
        if count > 0:
            category_scores[cat_id] = round(category_totals[cat_id] / count, 1)
        else:
            category_scores[cat_id] = 0.0

    return category_scores

def calculate_overall_privacy_risk(
    category_scores: Dict[str, float],
    custom_weights: Optional[Dict[str, float]] = None
) -> Tuple[float, str]:
    """
    Computes overall risk score from category scores using normalized weights.
    Returns: (overall_score, risk_level)
    """
    weights = custom_weights if custom_weights else DEFAULT_CATEGORY_WEIGHTS

    # Normalize weights so they sum to 1.0 even if user tweaked them
    total_weight = sum(weights.values())
    if total_weight <= 0:
        total_weight = 1.0

    weighted_score = 0.0
    for cat_id, score in category_scores.items():
        w = weights.get(cat_id, 0.0) / total_weight
        weighted_score += score * w

    overall_score = round(max(0.0, min(100.0, weighted_score)), 1)
    risk_level = classify_risk_level(overall_score)

    return overall_score, risk_level
