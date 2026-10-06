"""
JSON/CSV File Ingestion & Exported Profile Risk Analyzer
Evaluates synthetic or voluntarily exported profile metadata and post feeds
without live scraping, using rule-based and NLP keyword pattern recognition.
"""
import re
from typing import Dict, List, Any

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(\+?\d[\s\-\(\)]?){9,}")
WORKWORDS = {"badge", "id card", "hq", "office", "3rd floor", "desk", "shift", "corporation", "workplace"}
CHILD_HINTS = {"my kid", "my child", "daughter", "son", "little one", "#kids", "#school", "first day of school"}
ROUTINE_HINTS = {"every day", "daily", "7am run", "morning commute", "school drop", "every morning", "gym routine", "weekly shift"}

def analyze_json_profile(profile: Dict[str, Any], posts: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyzes profile.json and posts.json data contracts and generates a unified risk assessment.
    """
    findings: List[Dict[str, Any]] = []
    
    # 1. PII Exposure Analysis
    text_fields = " ".join([
        str(profile.get("bio", "")),
        str(profile.get("email", "") or ""),
        str(profile.get("phone", "") or ""),
        str(profile.get("display_name", ""))
    ])
    
    pii_score = 0.0
    if EMAIL_RE.search(text_fields):
        findings.append({
            "cat": "Personal Information",
            "severity": "HIGH",
            "item": "Email address exposed in bio or profile fields",
            "fix": "Remove public email; use a contact form or masked relay address."
        })
        pii_score += 40.0
        
    if PHONE_RE.search(text_fields):
        findings.append({
            "cat": "Personal Information",
            "severity": "CRITICAL",
            "item": "Phone number publicly visible on profile",
            "fix": "Remove phone number immediately to prevent SIM swap and smishing attacks."
        })
        pii_score += 50.0

    if profile.get("location"):
        findings.append({
            "cat": "Personal Information",
            "severity": "MEDIUM",
            "item": f"Residential/City location publicly disclosed: {profile.get('location')}",
            "fix": "Broaden location to country/region level or remove it from public view."
        })
        pii_score += 20.0
        
    pii_score = min(100.0, pii_score)

    # 2. Geolocation / Routine Analysis
    geo_score = 0.0
    for p in posts:
        pid = p.get("id", "post")
        if p.get("geo"):
            geo_score += 25.0
            findings.append({
                "cat": "Location Privacy",
                "severity": "HIGH",
                "item": f"Post {pid} contains precise coordinates/geotags",
                "fix": "Disable location services for camera/social app; avoid geotagging home/routine spots."
            })
        if p.get("media", {}).get("exif", {}).get("created_local"):
            geo_score += 15.0
            findings.append({
                "cat": "Location Privacy",
                "severity": "MEDIUM",
                "item": f"Post {pid} image leaks EXIF timestamp/hardware metadata",
                "fix": "Strip EXIF metadata from photos prior to uploading."
            })
        text = (p.get("text") or "").lower()
        if any(h in text for h in ROUTINE_HINTS):
            geo_score += 20.0
            findings.append({
                "cat": "Location Privacy",
                "severity": "HIGH",
                "item": f"Physical routine or recurring schedule disclosed in post {pid}",
                "fix": "Avoid broadcasting predictable schedules, morning routes, and recurring spots."
            })
    geo_score = min(100.0, geo_score)

    # 3. Children / Minors Analysis
    child_score = 0.0
    for p in posts:
        pid = p.get("id", "post")
        if p.get("media", {}).get("is_child_present"):
            child_score += 45.0
            findings.append({
                "cat": "Content Exposure",
                "severity": "CRITICAL",
                "item": f"Identifiable minor/child detected in public post {pid}",
                "fix": "Restrict post audience to approved close contacts or blur faces/school emblems."
            })
        text = (p.get("text") or "").lower()
        if any(h in text for h in CHILD_HINTS):
            child_score += 20.0
            findings.append({
                "cat": "Content Exposure",
                "severity": "MEDIUM",
                "item": f"Child or school references in post text ({pid})",
                "fix": "Avoid referencing school names, grades, or children's routines."
            })
    child_score = min(100.0, child_score)

    # 4. Workplace / Enterprise Security Analysis
    work_score = 0.0
    for p in posts:
        pid = p.get("id", "post")
        text = (p.get("text") or "").lower()
        if any(w in text for w in WORKWORDS):
            work_score += 35.0
            findings.append({
                "cat": "Workplace Security",
                "severity": "HIGH",
                "item": f"Workplace/badging/office details disclosed in post {pid}",
                "fix": "Avoid posting pictures of employee badges, office layouts, or computer screens."
            })
    work_score = min(100.0, work_score)

    # 5. Account Settings & Privacy Controls
    priv = profile.get("privacy", {})
    priv_score = 0.0
    if not priv.get("account_private", False):
        priv_score += 40.0
        findings.append({
            "cat": "Profile Visibility",
            "severity": "HIGH",
            "item": "Social profile account is public",
            "fix": "Toggle account to Private mode so only approved followers see posts."
        })
    if priv.get("show_activity", False):
        priv_score += 25.0
        findings.append({
            "cat": "Account Security",
            "severity": "LOW",
            "item": "Online activity and last-seen status is visible",
            "fix": "Turn off activity status to prevent active-hour tracking."
        })
    if priv.get("allow_message_requests", True):
        priv_score += 35.0
        findings.append({
            "cat": "Social Engineering",
            "severity": "MEDIUM",
            "item": "Open direct message requests from unknown accounts permitted",
            "fix": "Filter message requests from non-followers into a restricted folder."
        })
    priv_score = min(100.0, priv_score)

    # 6. Linkage & External Footprint
    link_score = 0.0
    for url in profile.get("links", []):
        url_lower = str(url).lower()
        if "linktr.ee" in url_lower or "pastebin" in url_lower:
            link_score += 35.0
            findings.append({
                "cat": "Digital Footprint",
                "severity": "MEDIUM",
                "item": f"Bio links to public aggregator: {url}",
                "fix": "Review aggregator links; verify they do not link to resumes with home address or phone."
            })
        if "github.com" in url_lower:
            link_score += 25.0
            findings.append({
                "cat": "Digital Footprint",
                "severity": "LOW",
                "item": "GitHub account linked in bio",
                "fix": "Audit public git commit history for personal emails or accidentally committed secrets."
            })
    link_score = min(100.0, link_score)

    # Composite Score Calculation (Weighted)
    weights = {
        "pii": 0.25,
        "geo": 0.20,
        "child": 0.15,
        "work": 0.15,
        "privacy": 0.15,
        "link": 0.10
    }
    
    overall_score = round(
        pii_score * weights["pii"] +
        geo_score * weights["geo"] +
        child_score * weights["child"] +
        work_score * weights["work"] +
        priv_score * weights["privacy"] +
        link_score * weights["link"],
        1
    )
    overall_score = min(100.0, max(0.0, overall_score))

    # Risk level classification
    if overall_score <= 20:
        risk_level = "LOW"
    elif overall_score <= 40:
        risk_level = "MODERATE"
    elif overall_score <= 70:
        risk_level = "HIGH"
    else:
        risk_level = "CRITICAL"

    return {
        "platform": profile.get("platform", "generic"),
        "username": profile.get("username", "anonymous"),
        "overall_score": overall_score,
        "risk_level": risk_level,
        "category_scores": {
            "Personal Information": pii_score,
            "Location Privacy": geo_score,
            "Content Exposure": child_score,
            "Workplace Security": work_score,
            "Privacy Settings": priv_score,
            "Digital Footprint": link_score
        },
        "findings": findings,
        "total_posts_analyzed": len(posts)
    }
