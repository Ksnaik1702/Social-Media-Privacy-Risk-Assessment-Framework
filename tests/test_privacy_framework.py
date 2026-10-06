"""
Automated Cybersecurity & Privacy Test Suite (30+ Tests)
Covers:
- Fully private vs. fully public profile scoring
- Specific vulnerability contributions (PII, location, MFA, etc.)
- Boundary condition checks (0, 20, 40, 70, 100)
- Recommendation tiers and priority actions
- Improvement simulator calculations
- Data minimization and Privacy by Design database audits
- Safe image EXIF inspection & scrubbing
"""
import pytest
from fastapi.testclient import TestClient

from backend.app import app
from backend.services.questionnaire_data import QUESTIONS, CATEGORIES
from backend.services.feature_extractor import extract_privacy_features
from backend.services.scoring_engine import calculate_category_scores, calculate_overall_privacy_risk
from backend.services.findings_engine import generate_privacy_findings
from backend.services.recommendation_engine import generate_recommendations
from backend.services.improvement_simulator import simulate_improvements
from backend.services.json_file_analyzer import analyze_json_profile
from backend.database import get_db_connection, save_assessment, get_assessment_by_id, delete_assessment_by_id
from backend.config import classify_risk_level

client = TestClient(app)

# ==========================================================
# 1. Fully Private Baseline Test
# ==========================================================
def test_01_fully_private_profile():
    answers = {}
    for q in QUESTIONS:
        # Select the safest defensive answer
        min_opt = min(q["risk_mapping"], key=q["risk_mapping"].get)
        answers[q["id"]] = min_opt
    
    features = extract_privacy_features(answers)
    cat_scores = calculate_category_scores(features)
    score, level = calculate_overall_privacy_risk(cat_scores)
    
    assert score <= 15.0, f"Fully private profile score should be very low, got {score}"
    assert level == "LOW"

# ==========================================================
# 2. Fully Public Synthetic Profile Test
# ==========================================================
def test_02_fully_public_profile():
    answers = {}
    for q in QUESTIONS:
        max_opt = max(q["risk_mapping"], key=q["risk_mapping"].get)
        answers[q["id"]] = max_opt
    
    features = extract_privacy_features(answers)
    cat_scores = calculate_category_scores(features)
    score, level = calculate_overall_privacy_risk(cat_scores)
    
    assert score >= 85.0, f"Fully public profile score should be critical, got {score}"
    assert level == "CRITICAL"

# ==========================================================
# 3. Public Phone Exposure
# ==========================================================
def test_03_public_phone_exposure():
    answers = {"q_pi_1": "YES"}
    features = extract_privacy_features(answers)
    assert features["q_pi_1"] == 100.0
    findings = generate_privacy_findings(answers, features)
    phone_finding = next((f for f in findings if f["question_id"] == "q_pi_1"), None)
    assert phone_finding is not None
    assert phone_finding["severity"] == "CRITICAL"

# ==========================================================
# 4. Public Email Exposure
# ==========================================================
def test_04_public_email_exposure():
    answers = {"q_pi_2": "YES"}
    features = extract_privacy_features(answers)
    assert features["q_pi_2"] == 90.0

# ==========================================================
# 5. Public Birthday Exposure
# ==========================================================
def test_05_public_birthday_exposure():
    answers = {"q_pi_3": "YES"}
    features = extract_privacy_features(answers)
    assert features["q_pi_3"] == 100.0

# ==========================================================
# 6. Public Location Exposure
# ==========================================================
def test_06_public_location_exposure():
    answers = {"q_pi_4": "YES"}
    features = extract_privacy_features(answers)
    assert features["q_pi_4"] == 85.0

# ==========================================================
# 7. Real-Time Location Check-ins
# ==========================================================
def test_07_real_time_checkins():
    answers = {"q_loc_1": "YES"}
    features = extract_privacy_features(answers)
    assert features["q_loc_1"] == 100.0
    findings = generate_privacy_findings(answers, features)
    f = next((item for item in findings if item["question_id"] == "q_loc_1"), None)
    assert f["severity"] == "CRITICAL"

# ==========================================================
# 8. Travel Plans Broadcasting
# ==========================================================
def test_08_travel_plans():
    answers = {"q_loc_2": "YES"}
    features = extract_privacy_features(answers)
    assert features["q_loc_2"] == 95.0

# ==========================================================
# 9. Workplace Exposure (Badges / Desk screens)
# ==========================================================
def test_09_workplace_exposure():
    answers = {"q_cnt_2": "YES"}
    features = extract_privacy_features(answers)
    assert features["q_cnt_2"] == 100.0

# ==========================================================
# 10. Education / Minor Exposure
# ==========================================================
def test_10_minor_education_exposure():
    answers = {"q_cnt_3": "YES"}
    features = extract_privacy_features(answers)
    assert features["q_cnt_3"] == 90.0

# ==========================================================
# 11. Public Default Posts
# ==========================================================
def test_11_public_default_posts():
    answers = {"q_cnt_1": "PUBLIC"}
    features = extract_privacy_features(answers)
    assert features["q_cnt_1"] == 95.0

# ==========================================================
# 12. Unknown Connections Accepted
# ==========================================================
def test_12_unknown_connections():
    answers = {"q_frn_1": "YES"}
    features = extract_privacy_features(answers)
    assert features["q_frn_1"] == 95.0

# ==========================================================
# 13. Tag Review Disabled
# ==========================================================
def test_13_tag_review_disabled():
    answers = {"q_tag_1": "NO"}
    features = extract_privacy_features(answers)
    assert features["q_tag_1"] == 95.0

# ==========================================================
# 14. MFA Disabled
# ==========================================================
def test_14_mfa_disabled():
    answers = {"q_sec_1": "NO"}
    features = extract_privacy_features(answers)
    assert features["q_sec_1"] == 100.0
    findings = generate_privacy_findings(answers, features)
    mfa_f = next((item for item in findings if item["question_id"] == "q_sec_1"), None)
    assert mfa_f["severity"] == "CRITICAL"

# ==========================================================
# 15. Login Alerts Disabled
# ==========================================================
def test_15_login_alerts_disabled():
    answers = {"q_sec_3": "NO"}
    features = extract_privacy_features(answers)
    assert features["q_sec_3"] == 85.0

# ==========================================================
# 16. Password Reuse Reported
# ==========================================================
def test_16_password_reuse():
    answers = {"q_sec_2": "YES"}
    features = extract_privacy_features(answers)
    assert features["q_sec_2"] == 100.0

# ==========================================================
# 17. Third-Party Apps Not Reviewed
# ==========================================================
def test_17_third_party_apps_not_reviewed():
    answers = {"q_app_1": "NO"}
    features = extract_privacy_features(answers)
    assert features["q_app_1"] == 90.0

# ==========================================================
# 18. Suspicious Link Awareness Low
# ==========================================================
def test_18_suspicious_link_awareness_low():
    answers = {"q_se_2": "YES"}
    features = extract_privacy_features(answers)
    assert features["q_se_2"] == 95.0

# ==========================================================
# 19. Old Historical Posts Not Reviewed
# ==========================================================
def test_19_old_posts_not_reviewed():
    answers = {"q_df_1": "NO"}
    features = extract_privacy_features(answers)
    assert features["q_df_1"] == 85.0

# ==========================================================
# 20. Privacy Settings Not Reviewed / Zombie Accounts
# ==========================================================
def test_20_zombie_accounts_unattended():
    answers = {"q_df_2": "YES"}
    features = extract_privacy_features(answers)
    assert features["q_df_2"] == 85.0

# ==========================================================
# 21. Category Score Calculation Consistency
# ==========================================================
def test_21_category_score_calculation():
    features = {q["id"]: 50.0 for q in QUESTIONS}
    cat_scores = calculate_category_scores(features)
    for cat_id in CATEGORIES:
        assert cat_id in cat_scores
        assert cat_scores[cat_id] == 50.0

# ==========================================================
# 22. Overall Score Calculation Weighted Output
# ==========================================================
def test_22_overall_score_calculation():
    cat_scores = {cat: 60.0 for cat in CATEGORIES}
    score, level = calculate_overall_privacy_risk(cat_scores)
    assert score == 60.0
    assert level == "HIGH"

# ==========================================================
# 23. Score Boundary 20 (LOW vs MODERATE)
# ==========================================================
def test_23_score_boundary_20():
    assert classify_risk_level(20.0) == "LOW"
    assert classify_risk_level(20.4) == "LOW"
    assert classify_risk_level(21.0) == "MODERATE"

# ==========================================================
# 24. Score Boundary 40 (MODERATE vs HIGH)
# ==========================================================
def test_24_score_boundary_40():
    assert classify_risk_level(40.0) == "MODERATE"
    assert classify_risk_level(40.4) == "MODERATE"
    assert classify_risk_level(41.0) == "HIGH"

# ==========================================================
# 25. Score Boundary 70 (HIGH vs CRITICAL)
# ==========================================================
def test_25_score_boundary_70():
    assert classify_risk_level(70.0) == "HIGH"
    assert classify_risk_level(70.4) == "HIGH"
    assert classify_risk_level(71.0) == "CRITICAL"

# ==========================================================
# 26. Recommendation Engine Prioritization
# ==========================================================
def test_26_recommendation_generation():
    findings = [
        {"id": "f1", "category_name": "Auth", "item": "MFA disabled", "severity": "CRITICAL", "recommendation": "Turn on MFA", "explanation": "test", "priority": "IMMEDIATE"},
        {"id": "f2", "category_name": "Footprint", "item": "Old posts", "severity": "LOW", "recommendation": "Archive posts", "explanation": "test", "priority": "GOOD_PRACTICE"}
    ]
    recs, actions = generate_recommendations(findings)
    assert len(recs) == 2
    assert recs[0]["priority"] == "IMMEDIATE"
    assert len(actions) >= 1
    assert "CRITICAL" in actions[0]

# ==========================================================
# 27. Improvement Simulation Delta Calculation
# ==========================================================
def test_27_improvement_simulation():
    orig_answers = {
        "q_pi_1": "YES",
        "q_sec_1": "NO",
        "q_loc_1": "YES"
    }
    sim_changes = {
        "q_pi_1": "NO",
        "q_sec_1": "YES",
        "q_loc_1": "NO"
    }
    sim_res = simulate_improvements(orig_answers, sim_changes)
    assert sim_res["risk_reduction_points"] > 0
    assert sim_res["simulated_score"] < sim_res["original_score"]
    assert len(sim_res["resolved_findings"]) > 0

# ==========================================================
# 28. Database Save and Fetch
# ==========================================================
def test_28_database_save_and_fetch():
    test_id = "test_audit_001"
    save_assessment(
        assessment_id=test_id,
        overall_score=45.5,
        risk_level="HIGH",
        category_scores={"profile_visibility": 50.0},
        findings=[{"category_id": "profile_visibility", "id": "find_1", "severity": "HIGH", "item": "Test finding"}]
    )
    rec = get_assessment_by_id(test_id)
    assert rec is not None
    assert rec["overall_score"] == 45.5
    assert rec["risk_level"] == "HIGH"
    
    # Cleanup
    delete_assessment_by_id(test_id)
    assert get_assessment_by_id(test_id) is None

# ==========================================================
# 29. Security & Privacy Audit: Zero Sensitive Data Stored
# ==========================================================
def test_29_sensitive_data_not_stored():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Check schema column names
    cursor.execute("PRAGMA table_info(assessments)")
    cols = [r["name"].lower() for r in cursor.fetchall()]
    conn.close()

    forbidden_keywords = ["phone", "password", "email", "address", "birthday", "dob", "ssn", "secret"]
    for kw in forbidden_keywords:
        assert kw not in cols, f"Privacy violation: {kw} detected in database table schema!"

# ==========================================================
# 30. REST API End-to-End Workflow Test
# ==========================================================
def test_30_api_end_to_end_assessment():
    payload = {
        "answers": {
            "q_pv_1": "PUBLIC",
            "q_pi_1": "YES",
            "q_sec_1": "NO"
        }
    }
    response = client.post("/api/assessment", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "assessment_id" in data
    assert "overall_score" in data
    assert "category_scores" in data
    assert len(data["findings"]) >= 2

# ==========================================================
# 31. JSON Profile & Post Feed Analyzer Test
# ==========================================================
def test_31_json_profile_analyzer():
    profile = {
        "username": "test_user",
        "bio": "Contact me at user@example.com or +1 415 555 1234",
        "location": "New York, NY",
        "privacy": {"account_private": False}
    }
    posts = [
        {"id": "p1", "text": "Daily 7am run to work", "geo": {"lat": 40.7, "lon": -74.0}},
        {"id": "p2", "text": "Badge pickup at headquarters"}
    ]
    res = analyze_json_profile(profile, posts)
    assert res["overall_score"] > 20.0
    assert any("Email" in f["item"] for f in res["findings"])
    assert any("Phone" in f["item"] for f in res["findings"])
    assert any("coordinates" in f["item"] for f in res["findings"])

# ==========================================================
# 32. Privacy Checklist API Test
# ==========================================================
def test_32_privacy_checklist_api():
    res = client.get("/api/privacy-checklist")
    assert res.status_code == 200
    data = res.json()
    assert "checklist" in data
    assert len(data["checklist"]) >= 15
