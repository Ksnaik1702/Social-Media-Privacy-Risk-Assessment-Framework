"""
Privacy Improvement Simulator
Simulates the impact of applying defensive privacy hardening steps.
Calculates before/after scores, delta point reduction, and resolved weaknesses.
"""
from typing import Dict, List, Any
from backend.services.feature_extractor import extract_privacy_features
from backend.services.scoring_engine import calculate_category_scores, calculate_overall_privacy_risk
from backend.services.findings_engine import generate_privacy_findings

def simulate_improvements(
    original_answers: Dict[str, str],
    simulated_changes: Dict[str, str],
    custom_weights: Dict[str, float] = None
) -> Dict[str, Any]:
    """
    Simulates applying proposed privacy setting improvements.
    Returns delta metrics, category shifts, and resolved findings list.
    """
    # 1. Baseline assessment
    orig_features = extract_privacy_features(original_answers)
    orig_cat_scores = calculate_category_scores(orig_features)
    orig_score, orig_level = calculate_overall_privacy_risk(orig_cat_scores, custom_weights)
    orig_findings = generate_privacy_findings(original_answers, orig_features)

    # 2. Simulated scenario
    merged_answers = dict(original_answers)
    merged_answers.update(simulated_changes)

    sim_features = extract_privacy_features(merged_answers)
    sim_cat_scores = calculate_category_scores(sim_features)
    sim_score, sim_level = calculate_overall_privacy_risk(sim_cat_scores, custom_weights)
    sim_findings = generate_privacy_findings(merged_answers, sim_features)

    # 3. Deltas
    risk_reduction_points = round(orig_score - sim_score, 1)
    risk_reduction_percent = round((risk_reduction_points / orig_score * 100), 1) if orig_score > 0 else 0.0

    # 4. Resolved findings tracking
    sim_finding_ids = {f["id"] for f in sim_findings}
    resolved_findings = [
        f["item"] for f in orig_findings if f["id"] not in sim_finding_ids
    ]

    # 5. Category-wise comparison
    category_comparison = {}
    for cat_id in orig_cat_scores:
        category_comparison[cat_id] = {
            "before": orig_cat_scores[cat_id],
            "after": sim_cat_scores.get(cat_id, 0.0),
            "reduction": round(orig_cat_scores[cat_id] - sim_cat_scores.get(cat_id, 0.0), 1)
        }

    return {
        "original_score": orig_score,
        "original_risk_level": orig_level,
        "simulated_score": sim_score,
        "simulated_risk_level": sim_level,
        "risk_reduction_points": risk_reduction_points,
        "risk_reduction_percent": risk_reduction_percent,
        "category_comparison": category_comparison,
        "resolved_findings": resolved_findings,
        "disclaimer": "Educational simulation based on rubric weights. Real-world privacy requires ongoing behavioral caution and platform policy enforcement."
    }
