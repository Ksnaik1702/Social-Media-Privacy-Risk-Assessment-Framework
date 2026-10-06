"""
Batch Assessment CLI Tool
Processes exported or synthetic sample profile folders and generates a summary CSV report.
Usage: python batch_assess.py
"""
import json
import csv
from pathlib import Path
from backend.services.json_file_analyzer import analyze_json_profile

BASE_DIR = Path(__file__).resolve().parent
SAMPLES_DIR = BASE_DIR / "data" / "sample_profiles"
OUTPUT_REPORT = BASE_DIR / "reports" / "batch_privacy_report.csv"

def run_batch_assessment():
    print("[*] Running Batch Profile Assessment across sample profiles...")
    OUTPUT_REPORT.parent.mkdir(exist_ok=True)
    
    rows = []
    sample_folders = [f for f in SAMPLES_DIR.iterdir() if f.is_dir()]
    
    if not sample_folders:
        print("[!] No sample folders found in data/sample_profiles")
        return

    for folder in sample_folders:
        prof_file = folder / "profile.json"
        posts_file = folder / "posts.json"
        
        if prof_file.exists():
            with open(prof_file, "r", encoding="utf-8") as f:
                prof = json.load(f)
            posts = []
            if posts_file.exists():
                with open(posts_file, "r", encoding="utf-8") as f:
                    posts = json.load(f)
                    
            res = analyze_json_profile(prof, posts)
            rows.append({
                "cohort_folder": folder.name,
                "platform": res.get("platform", "generic"),
                "username": res.get("username", "anonymous"),
                "overall_score": res["overall_score"],
                "risk_level": res["risk_level"],
                "pii_score": res["category_scores"].get("Personal Information", 0.0),
                "geo_score": res["category_scores"].get("Location Privacy", 0.0),
                "total_findings": len(res["findings"]),
                "total_posts_analyzed": res["total_posts_analyzed"]
            })

    if rows:
        with open(OUTPUT_REPORT, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        print(f"[+] Successfully wrote batch privacy report to: {OUTPUT_REPORT}")
        for r in rows:
            print(f"    - [{r['risk_level']}] {r['cohort_folder']} ({r['username']}): Score = {r['overall_score']}/100, Findings = {r['total_findings']}")

if __name__ == "__main__":
    run_batch_assessment()
