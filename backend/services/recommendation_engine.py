"""
Privacy Recommendation Engine
Processes findings into tailored, prioritized remediation steps.
Tiers recommendations into:
1. IMMEDIATE (Critical threats like exposed phone, disabled MFA, real-time check-ins)
2. IMPORTANT (High threats like public posts, unvetted connections, travel itineraries)
3. GOOD PRACTICE (Medium/low hygiene like tag reviews, old post purges, app audits)
"""
from typing import List, Dict, Any, Tuple

def generate_recommendations(findings: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[str]]:
    """
    Groups recommendations by priority tier and compiles top immediate action items.
    Returns: (structured_recommendations, top_priority_actions)
    """
    immediate = []
    important = []
    good_practice = []

    for f in findings:
        rec_entry = {
            "finding_id": f["id"],
            "category": f["category_name"],
            "issue": f["item"],
            "severity": f["severity"],
            "recommendation": f["recommendation"],
            "explanation": f["explanation"],
            "priority": f["priority"]
        }

        if f["priority"] == "IMMEDIATE":
            immediate.append(rec_entry)
        elif f["priority"] == "IMPORTANT":
            important.append(rec_entry)
        else:
            good_practice.append(rec_entry)

    # Top priority action strings for quick executive glance
    top_actions = []
    for item in immediate:
        top_actions.append(f"CRITICAL: {item['recommendation']}")
    for item in important[:3]:
        top_actions.append(f"HIGH: {item['recommendation']}")

    if not top_actions:
        top_actions.append("Maintain existing defensive privacy settings with quarterly reviews.")

    all_recommendations = immediate + important + good_practice
    return all_recommendations, top_actions
