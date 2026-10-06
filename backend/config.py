"""
Application Configuration
Centralized settings for weights, thresholds, database path, and CORS.
"""
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "privacy_assessment.db"
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

# Default Risk Category Weights (Sum = 100%)
DEFAULT_CATEGORY_WEIGHTS = {
    "profile_visibility": 0.10,
    "personal_information": 0.15,
    "location_privacy": 0.15,
    "posts_content": 0.10,
    "friends_followers": 0.10,
    "tagging_mentions": 0.05,
    "account_security": 0.15,
    "third_party_apps": 0.05,
    "social_engineering": 0.10,
    "digital_footprint": 0.05,
}

# Risk Level Classification Thresholds
# Educational risk scale: 0-100 where higher score = higher assessed exposure/risk
RISK_LEVEL_THRESHOLDS = {
    "LOW": (0, 20),
    "MODERATE": (21, 40),
    "HIGH": (41, 70),
    "CRITICAL": (71, 100),
}

def classify_risk_level(score: float) -> str:
    """Classify numerical score into risk level tier."""
    rounded_score = round(score)
    if rounded_score <= 20:
        return "LOW"
    elif rounded_score <= 40:
        return "MODERATE"
    elif rounded_score <= 70:
        return "HIGH"
    else:
        return "CRITICAL"
