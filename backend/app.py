"""
Main FastAPI Application Entrypoint
Mounts REST API routes and static frontend files.
"""
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.routes.api import router as api_router
from backend.database import init_db

# Initialize database schema
init_db()

app = FastAPI(
    title="Social Media Privacy Risk Assessment Framework",
    description="A defensive cybersecurity and privacy engineering platform evaluating online exposure, account security, and digital footprints.",
    version="1.0.0"
)

# Enable CORS for development and cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Router
app.include_router(api_router)

# Mount Frontend static files
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

@app.get("/")
def serve_index():
    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"message": "Social Media Privacy Risk Assessment Framework API is running. Access /docs for interactive documentation."}

@app.get("/assessment")
def serve_assessment():
    return FileResponse(FRONTEND_DIR / "assessment.html")

@app.get("/dashboard")
def serve_dashboard():
    return FileResponse(FRONTEND_DIR / "dashboard.html")

@app.get("/metadata")
def serve_metadata():
    return FileResponse(FRONTEND_DIR / "metadata.html")
