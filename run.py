"""
Social Media Privacy Risk Assessment Framework - Application Launcher
Runs backend FastAPI server with mounted frontend static UI.
Usage: python run.py
"""
import uvicorn
from pathlib import Path
from backend.database import init_db
from data.generate_dataset import generate_synthetic_dataset

def main():
    print("=" * 70)
    print("  SOCIAL MEDIA PRIVACY RISK ASSESSMENT FRAMEWORK")
    print("  Defensive Cybersecurity & Privacy Engineering Project")
    print("=" * 70)

    # 1. Initialize SQLite Database
    print("[1/3] Initializing SQLite database schema...")
    init_db()

    # 2. Check / Generate Synthetic Dataset
    csv_path = Path(__file__).resolve().parent / "data" / "social_media_privacy_assessments.csv"
    if not csv_path.exists():
        print("[2/3] Generating 1,200 synthetic assessment benchmark records...")
        generate_synthetic_dataset(1200)
    else:
        print("[2/3] Benchmark synthetic dataset detected (1,200 records).")

    # 3. Launch Server
    print("[3/3] Starting PrivacyGuard server...")
    print("-" * 70)
    print("  -> Web Application:        http://127.0.0.1:8000")
    print("  -> Privacy Assessment:     http://127.0.0.1:8000/assessment")
    print("  -> Interactive Dashboard:  http://127.0.0.1:8000/dashboard")
    print("  -> EXIF Metadata Tool:     http://127.0.0.1:8000/metadata")
    print("  -> REST API Docs:          http://127.0.0.1:8000/docs")
    print("-" * 70)
    print("Press CTRL+C to stop the server.")

    uvicorn.run("backend.app:app", host="127.0.0.1", port=8000, reload=False)

if __name__ == "__main__":
    main()
