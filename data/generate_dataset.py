"""
Synthetic Profile Dataset Generator
Generates 1,000+ realistic, fictional privacy risk assessment records.
Ethical & Defensive: Generates purely synthetic data with NO real individuals or scraping.
Saves to data/social_media_privacy_assessments.csv.
"""
import random
import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent
OUTPUT_CSV = DATA_DIR / "social_media_privacy_assessments.csv"

def generate_synthetic_dataset(num_records: int = 1200) -> str:
    random.seed(42)  # Deterministic seed for scientific reproducibility

    records = []
    
    # Archetype weights for realistic distribution:
    # 25% Privacy Conscious, 40% Average Casual, 25% High Exposure, 10% Critical/Vulnerable
    archetypes = [
        ("conscious", 0.25),
        ("casual", 0.40),
        ("high_exposure", 0.25),
        ("critical", 0.10)
    ]

    for i in range(1, num_records + 1):
        pid = f"SYNTH_USER_{i:04d}"
        
        # Pick archetype based on distribution
        r_val = random.random()
        if r_val < 0.25:
            arch = "conscious"
        elif r_val < 0.65:
            arch = "casual"
        elif r_val < 0.90:
            arch = "high_exposure"
        else:
            arch = "critical"

        if arch == "conscious":
            profile_visibility = random.choices(["PRIVATE", "FRIENDS", "PUBLIC"], weights=[0.70, 0.25, 0.05])[0]
            phone_public = random.choices(["NO", "YES"], weights=[0.95, 0.05])[0]
            email_public = random.choices(["NO", "YES"], weights=[0.90, 0.10])[0]
            birthday_public = random.choices(["NO", "SOMETIMES", "YES"], weights=[0.85, 0.10, 0.05])[0]
            location_public = random.choices(["NO", "SOMETIMES", "YES"], weights=[0.85, 0.10, 0.05])[0]
            workplace_public = random.choices(["NO", "YES"], weights=[0.80, 0.20])[0]
            education_public = random.choices(["NO", "YES"], weights=[0.75, 0.25])[0]
            relationship_public = random.choices(["NO", "YES"], weights=[0.85, 0.15])[0]
            posts_public = random.choices(["PRIVATE", "FRIENDS", "PUBLIC"], weights=[0.60, 0.35, 0.05])[0]
            location_tagging = random.choices(["NO", "SOMETIMES", "YES"], weights=[0.85, 0.10, 0.05])[0]
            travel_posts = random.choices(["NO", "SOMETIMES", "YES"], weights=[0.85, 0.10, 0.05])[0]
            unknown_connections = random.choices(["NO", "SOMETIMES", "YES"], weights=[0.90, 0.08, 0.02])[0]
            tag_review_enabled = random.choices(["YES", "NO"], weights=[0.90, 0.10])[0]
            third_party_apps_reviewed = random.choices(["YES", "NO"], weights=[0.85, 0.15])[0]
            mfa_enabled = random.choices(["YES", "NO"], weights=[0.95, 0.05])[0]
            login_alerts_enabled = random.choices(["YES", "NO"], weights=[0.90, 0.10])[0]
            password_reuse_reported = random.choices(["NO", "SOMETIMES", "YES"], weights=[0.90, 0.08, 0.02])[0]
            suspicious_link_awareness = random.choices(["HIGH", "MEDIUM", "LOW"], weights=[0.85, 0.12, 0.03])[0]
            old_posts_reviewed = random.choices(["YES", "SOMETIMES", "NO"], weights=[0.70, 0.20, 0.10])[0]
            privacy_settings_reviewed = random.choices(["YES", "SOMETIMES", "NO"], weights=[0.80, 0.15, 0.05])[0]

        elif arch == "casual":
            profile_visibility = random.choices(["FRIENDS", "PUBLIC", "PRIVATE"], weights=[0.60, 0.25, 0.15])[0]
            phone_public = random.choices(["NO", "YES"], weights=[0.75, 0.25])[0]
            email_public = random.choices(["NO", "YES"], weights=[0.65, 0.35])[0]
            birthday_public = random.choices(["SOMETIMES", "YES", "NO"], weights=[0.40, 0.35, 0.25])[0]
            location_public = random.choices(["SOMETIMES", "YES", "NO"], weights=[0.45, 0.30, 0.25])[0]
            workplace_public = random.choices(["YES", "NO"], weights=[0.50, 0.50])[0]
            education_public = random.choices(["YES", "NO"], weights=[0.55, 0.45])[0]
            relationship_public = random.choices(["YES", "NO"], weights=[0.45, 0.55])[0]
            posts_public = random.choices(["FRIENDS", "PUBLIC", "PRIVATE"], weights=[0.60, 0.30, 0.10])[0]
            location_tagging = random.choices(["SOMETIMES", "YES", "NO"], weights=[0.45, 0.30, 0.25])[0]
            travel_posts = random.choices(["SOMETIMES", "YES", "NO"], weights=[0.50, 0.30, 0.20])[0]
            unknown_connections = random.choices(["SOMETIMES", "NO", "YES"], weights=[0.45, 0.40, 0.15])[0]
            tag_review_enabled = random.choices(["NO", "YES"], weights=[0.55, 0.45])[0]
            third_party_apps_reviewed = random.choices(["NO", "YES"], weights=[0.60, 0.40])[0]
            mfa_enabled = random.choices(["YES", "NO"], weights=[0.65, 0.35])[0]
            login_alerts_enabled = random.choices(["YES", "NO"], weights=[0.55, 0.45])[0]
            password_reuse_reported = random.choices(["SOMETIMES", "YES", "NO"], weights=[0.45, 0.30, 0.25])[0]
            suspicious_link_awareness = random.choices(["MEDIUM", "HIGH", "LOW"], weights=[0.60, 0.25, 0.15])[0]
            old_posts_reviewed = random.choices(["SOMETIMES", "NO", "YES"], weights=[0.40, 0.40, 0.20])[0]
            privacy_settings_reviewed = random.choices(["SOMETIMES", "NO", "YES"], weights=[0.45, 0.35, 0.20])[0]

        elif arch == "high_exposure":
            profile_visibility = random.choices(["PUBLIC", "FRIENDS"], weights=[0.80, 0.20])[0]
            phone_public = random.choices(["YES", "NO"], weights=[0.60, 0.40])[0]
            email_public = random.choices(["YES", "NO"], weights=[0.80, 0.20])[0]
            birthday_public = random.choices(["YES", "SOMETIMES", "NO"], weights=[0.75, 0.15, 0.10])[0]
            location_public = random.choices(["YES", "SOMETIMES", "NO"], weights=[0.80, 0.15, 0.05])[0]
            workplace_public = random.choices(["YES", "NO"], weights=[0.85, 0.15])[0]
            education_public = random.choices(["YES", "NO"], weights=[0.80, 0.20])[0]
            relationship_public = random.choices(["YES", "NO"], weights=[0.70, 0.30])[0]
            posts_public = random.choices(["PUBLIC", "FRIENDS"], weights=[0.85, 0.15])[0]
            location_tagging = random.choices(["YES", "SOMETIMES", "NO"], weights=[0.75, 0.20, 0.05])[0]
            travel_posts = random.choices(["YES", "SOMETIMES", "NO"], weights=[0.80, 0.15, 0.05])[0]
            unknown_connections = random.choices(["YES", "SOMETIMES", "NO"], weights=[0.70, 0.25, 0.05])[0]
            tag_review_enabled = random.choices(["NO", "YES"], weights=[0.85, 0.15])[0]
            third_party_apps_reviewed = random.choices(["NO", "YES"], weights=[0.85, 0.15])[0]
            mfa_enabled = random.choices(["NO", "YES"], weights=[0.65, 0.35])[0]
            login_alerts_enabled = random.choices(["NO", "YES"], weights=[0.75, 0.25])[0]
            password_reuse_reported = random.choices(["YES", "SOMETIMES", "NO"], weights=[0.65, 0.25, 0.10])[0]
            suspicious_link_awareness = random.choices(["LOW", "MEDIUM", "HIGH"], weights=[0.55, 0.35, 0.10])[0]
            old_posts_reviewed = random.choices(["NO", "SOMETIMES", "YES"], weights=[0.75, 0.20, 0.05])[0]
            privacy_settings_reviewed = random.choices(["NO", "SOMETIMES", "YES"], weights=[0.80, 0.15, 0.05])[0]

        else:  # critical
            profile_visibility = "PUBLIC"
            phone_public = "YES"
            email_public = "YES"
            birthday_public = "YES"
            location_public = "YES"
            workplace_public = "YES"
            education_public = "YES"
            relationship_public = "YES"
            posts_public = "PUBLIC"
            location_tagging = "YES"
            travel_posts = "YES"
            unknown_connections = "YES"
            tag_review_enabled = "NO"
            third_party_apps_reviewed = "NO"
            mfa_enabled = "NO"
            login_alerts_enabled = "NO"
            password_reuse_reported = "YES"
            suspicious_link_awareness = "LOW"
            old_posts_reviewed = "NO"
            privacy_settings_reviewed = "NO"

        # Calculate normalized synthetic risk score (0 - 100)
        # Higher score = HIGHER risk
        score = 0.0
        
        # Profile & Visibility (15 pts)
        if profile_visibility == "PUBLIC": score += 10.0
        elif profile_visibility == "FRIENDS": score += 3.0
        if posts_public == "PUBLIC": score += 5.0
        elif posts_public == "FRIENDS": score += 2.0

        # PII exposure (25 pts)
        if phone_public == "YES": score += 8.0
        if email_public == "YES": score += 6.0
        if birthday_public == "YES": score += 6.0
        elif birthday_public == "SOMETIMES": score += 3.0
        if relationship_public == "YES": score += 3.0
        if workplace_public == "YES": score += 2.0

        # Location exposure (20 pts)
        if location_public == "YES": score += 7.0
        elif location_public == "SOMETIMES": score += 3.0
        if location_tagging == "YES": score += 7.0
        elif location_tagging == "SOMETIMES": score += 3.0
        if travel_posts == "YES": score += 6.0
        elif travel_posts == "SOMETIMES": score += 3.0

        # Account Security (20 pts)
        if mfa_enabled == "NO": score += 8.0
        if password_reuse_reported == "YES": score += 6.0
        elif password_reuse_reported == "SOMETIMES": score += 3.0
        if login_alerts_enabled == "NO": score += 6.0

        # Behavioral & Social Engineering (20 pts)
        if unknown_connections == "YES": score += 5.0
        elif unknown_connections == "SOMETIMES": score += 2.0
        if tag_review_enabled == "NO": score += 4.0
        if third_party_apps_reviewed == "NO": score += 4.0
        if suspicious_link_awareness == "LOW": score += 4.0
        elif suspicious_link_awareness == "MEDIUM": score += 2.0
        if old_posts_reviewed == "NO": score += 3.0

        # Add minor realistic noise (+/- 2 pts)
        score += random.uniform(-2.0, 2.0)
        score = round(max(0.0, min(100.0, score)), 1)

        # Risk classification
        if score <= 20.0:
            risk_level = "LOW"
        elif score <= 40.0:
            risk_level = "MODERATE"
        elif score <= 70.0:
            risk_level = "HIGH"
        else:
            risk_level = "CRITICAL"

        records.append({
            "profile_id": pid,
            "profile_visibility": profile_visibility,
            "phone_public": phone_public,
            "email_public": email_public,
            "birthday_public": birthday_public,
            "location_public": location_public,
            "workplace_public": workplace_public,
            "education_public": education_public,
            "relationship_public": relationship_public,
            "posts_public": posts_public,
            "location_tagging": location_tagging,
            "travel_posts": travel_posts,
            "unknown_connections": unknown_connections,
            "tag_review_enabled": tag_review_enabled,
            "third_party_apps_reviewed": third_party_apps_reviewed,
            "mfa_enabled": mfa_enabled,
            "login_alerts_enabled": login_alerts_enabled,
            "password_reuse_reported": password_reuse_reported,
            "suspicious_link_awareness": suspicious_link_awareness,
            "old_posts_reviewed": old_posts_reviewed,
            "privacy_settings_reviewed": privacy_settings_reviewed,
            "risk_score": score,
            "risk_level": risk_level
        })

    # Write to CSV
    fieldnames = list(records[0].keys())
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"[+] Successfully generated {len(records)} synthetic records into {OUTPUT_CSV}")
    return str(OUTPUT_CSV)

if __name__ == "__main__":
    generate_synthetic_dataset(1200)
