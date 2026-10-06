"""
Privacy-Preserving Database Storage (SQLite)
Architected with Privacy by Design:
- Data Minimization: Stores only assessment scores, finding identifiers, and aggregate metrics.
- Zero PII: Does not store personal phone numbers, addresses, emails, or credentials.
"""
import sqlite3
import json
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from backend.config import DATABASE_PATH

def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables according to Privacy by Design schema."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Assessments Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assessments (
        assessment_id TEXT PRIMARY KEY,
        created_at TEXT NOT NULL,
        overall_score REAL NOT NULL,
        risk_level TEXT NOT NULL,
        source_type TEXT DEFAULT 'questionnaire'
    )
    """)

    # Category Scores Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS category_scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        assessment_id TEXT NOT NULL,
        category TEXT NOT NULL,
        score REAL NOT NULL,
        FOREIGN KEY (assessment_id) REFERENCES assessments (assessment_id) ON DELETE CASCADE
    )
    """)

    # Findings Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS findings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        assessment_id TEXT NOT NULL,
        category TEXT NOT NULL,
        finding_id TEXT NOT NULL,
        severity TEXT NOT NULL,
        description TEXT NOT NULL,
        FOREIGN KEY (assessment_id) REFERENCES assessments (assessment_id) ON DELETE CASCADE
    )
    """)

    conn.commit()
    conn.close()

def save_assessment(
    assessment_id: str,
    overall_score: float,
    risk_level: str,
    category_scores: Dict[str, float],
    findings: List[Dict[str, Any]],
    source_type: str = "questionnaire"
):
    """Save an assessment using data-minimized fields."""
    conn = get_db_connection()
    cursor = conn.cursor()
    created_at = datetime.now(timezone.utc).isoformat()

    cursor.execute(
        "INSERT INTO assessments (assessment_id, created_at, overall_score, risk_level, source_type) VALUES (?, ?, ?, ?, ?)",
        (assessment_id, created_at, overall_score, risk_level, source_type)
    )

    for cat, score in category_scores.items():
        cursor.execute(
            "INSERT INTO category_scores (assessment_id, category, score) VALUES (?, ?, ?)",
            (assessment_id, cat, score)
        )

    for f in findings:
        cursor.execute(
            "INSERT INTO findings (assessment_id, category, finding_id, severity, description) VALUES (?, ?, ?, ?, ?)",
            (assessment_id, f.get("category_id", "general"), f.get("id", "finding"), f.get("severity", "MEDIUM"), f.get("item", ""))
        )

    conn.commit()
    conn.close()

def get_assessment_by_id(assessment_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve an assessment by ID without sensitive personal data."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM assessments WHERE assessment_id = ?", (assessment_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None

    assessment = dict(row)

    cursor.execute("SELECT category, score FROM category_scores WHERE assessment_id = ?", (assessment_id,))
    cat_rows = cursor.fetchall()
    assessment["category_scores"] = {r["category"]: r["score"] for r in cat_rows}

    cursor.execute("SELECT category, finding_id, severity, description FROM findings WHERE assessment_id = ?", (assessment_id,))
    findings_rows = cursor.fetchall()
    assessment["findings"] = [dict(r) for r in findings_rows]

    conn.close()
    return assessment

def delete_assessment_by_id(assessment_id: str) -> bool:
    """Support right to erasure (data deletion)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM assessments WHERE assessment_id = ?", (assessment_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

def get_dashboard_statistics() -> Dict[str, Any]:
    """Calculate aggregate stats across all assessments."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*), AVG(overall_score) FROM assessments")
    count, avg_score = cursor.fetchone()
    count = count or 0
    avg_score = round(avg_score, 1) if avg_score is not None else 0.0

    # Risk level distribution
    cursor.execute("SELECT risk_level, COUNT(*) FROM assessments GROUP BY risk_level")
    dist = {"LOW": 0, "MODERATE": 0, "HIGH": 0, "CRITICAL": 0}
    for r in cursor.fetchall():
        if r["risk_level"] in dist:
            dist[r["risk_level"]] = r[1]

    # Top weaknesses across findings
    cursor.execute("""
        SELECT description, severity, COUNT(*) as count 
        FROM findings 
        GROUP BY description, severity 
        ORDER BY count DESC 
        LIMIT 6
    """)
    top_weaknesses = [{"item": r["description"], "severity": r["severity"], "count": r["count"]} for r in cursor.fetchall()]

    # Recent assessments
    cursor.execute("""
        SELECT assessment_id, created_at, overall_score, risk_level, source_type 
        FROM assessments 
        ORDER BY created_at DESC 
        LIMIT 10
    """)
    recent = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return {
        "total_assessments": count,
        "average_score": avg_score,
        "risk_distribution": dist,
        "top_weaknesses": top_weaknesses,
        "recent_assessments": recent
    }
