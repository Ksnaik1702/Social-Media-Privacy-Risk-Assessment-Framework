# Social Media Privacy Risk Assessment Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-green.svg)](https://python.org)
[![Framework](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![Tests](https://img.shields.io/badge/Tests-32%20Passed-brightgreen.svg)]()
[![Privacy by Design](https://img.shields.io/badge/Standard-Privacy%20by%20Design-purple.svg)]()

> **Defensive Cybersecurity Course Project:** An industry-oriented privacy risk evaluation platform that assesses social-media exposure, account-security practices, social-engineering susceptibility, and digital-footprint risks using self-reported configurations and synthetic data.

---

## 🛡️ Ethical & Defensive Security Notice

> **IMPORTANT:** This project is strictly designed for **defensive cybersecurity education and privacy awareness**.
> - **Zero Scraping:** It does **NOT** scrape real social media profiles.
> - **Zero Tracking:** It does **NOT** collect private information about real individuals or perform account enumeration.
> - **Zero Sensitive Storage:** It does **NOT** ask for or store passwords, actual phone numbers, email addresses, or private messages.
> - **Voluntary & Synthetic:** It evaluates voluntarily provided questionnaire responses and synthetic demo profiles only.
> - **Educational Risk Framework:** A high score indicates higher assessed exposure; it does not constitute a legal or technical guarantee against account compromise.

---

## Table of Contents
1. [Overview & Problem Statement](#overview--problem-statement)
2. [Cybersecurity & Industry Relevance](#cybersecurity--industry-relevance)
3. [Privacy vs. Security](#privacy-vs-security)
4. [Key Features](#key-features)
5. [System Architecture](#system-architecture)
6. [Technology Stack](#technology-stack)
7. [The 45-Question Assessment & 10 Risk Categories](#the-45-question-assessment--10-risk-categories)
8. [Risk Scoring Engine & Rubric](#risk-scoring-engine--rubric)
9. [Privacy Improvement Simulator](#privacy-improvement-simulator)
10. [Photo EXIF Metadata Inspector & Scrubber](#photo-exif-metadata-inspector--scrubber)
11. [Privacy by Design & Safe Storage](#privacy-by-design--safe-storage)
12. [Installation & Local Execution](#installation--local-execution)
13. [REST API Documentation](#rest-api-documentation)
14. [Automated Testing Suite (32 Tests)](#automated-testing-suite-32-tests)
15. [Documentation & Proof of Work Artifacts](#documentation--proof-of-work-artifacts)
16. [License & Author](#license--author)

---

## Overview & Problem Statement

### The Problem
Modern social media platforms are optimized for engagement and broad discoverability, frequently leading users to inadvertently overshare personal landmarks, workplace environments, and routine schedules. Threat actors routinely conduct **Open-Source Intelligence (OSINT)** reconnaissance across these public breadcrumbs to execute:
- **Credential Stuffing & Account Takeover** (facilitated by password reuse and disabled MFA).
- **SIM Swapping & Smishing** (facilitated by public phone numbers in bios).
- **Spear Phishing & Pretexting** (facilitated by workplace ID badging and family references).
- **Physical Burglary & Stalking** (facilitated by real-time location check-ins and embedded image GPS EXIF tags).

### The Objective
Build a transparent, defensible, and non-invasive privacy diagnostic platform that:
1. Ingests self-reported configuration answers or synthetic profile/post feeds.
2. Evaluates exposure across 10 security domains without collecting real PII.
3. Computes explainable 0–100 category scores and an overall Privacy Risk Score.
4. Generates prioritized, actionable remediation steps.
5. Simulates the defensive impact of privacy hardening via an interactive "What-If" simulator.

---

## Cybersecurity & Industry Relevance

This project demonstrates core capabilities expected in industry cybersecurity roles:

| Industry Role | Project Alignment |
| :--- | :--- |
| **Cybersecurity Analyst** | Threat modeling social engineering vectors, identifying PII exposure paths, auditing account authentication controls. |
| **Privacy Analyst / Engineer** | Enforcing Privacy by Design, data minimization principles, least privilege OAuth review, and GDPR right to erasure. |
| **GRC Analyst** | Developing structured risk scoring rubrics, policy compliance checklists, and risk reduction metrics. |
| **SOC Analyst / Threat Intel** | Understanding adversary OSINT reconnaissance techniques and mapping digital breadcrumbs to attack stages. |
| **Security Awareness Specialist** | Delivering actionable security coaching, interactive "What-If" simulation, and employee training artifacts. |

---

## Privacy vs. Security

A foundational pillar of this framework is the distinction between privacy and security:

```
┌─────────────────────────────────────────┐     ┌─────────────────────────────────────────┐
│                 PRIVACY                 │     │                SECURITY                 │
├─────────────────────────────────────────┤     ├─────────────────────────────────────────┤
│ Controls how personal information is    │     │ Protects systems, accounts, and data   │
│ collected, exposed, shared, and used.   │     │ from unauthorized access or compromise. │
│                                         │     │                                         │
│ Focus: Data minimization, visibility,   │     │ Focus: Encryption, MFA, strong unique   │
│ audience limits, consent boundaries.    │     │ passwords, session management.          │
└─────────────────────────────────────────┘     └─────────────────────────────────────────┘
```

> **Core Principle:** **Strong Account Security ≠ Strong Privacy.**
> An account can have a 30-character random password and hardware-token MFA (high security), yet still publicly display the user's home neighborhood, phone number, and real-time travel plans (critical privacy risk). Both dimensions must be evaluated.

---

## Key Features

1. **45-Question Diagnostic Assessment:** Evaluates social media habits and settings across 10 distinct security categories.
2. **0–100 Weighted Risk Scoring Engine:** Higher score = higher exposure/risk. Transparent categorization: LOW (0–20), MODERATE (21–40), HIGH (41–70), CRITICAL (71–100).
3. **Interactive Privacy Improvement Simulator:** "What-If" analysis allowing users to toggle proposed hardening settings and see live risk score reductions and resolved weaknesses.
4. **Local EXIF Metadata Inspector & Scrubber:** Parses photo GPS coordinates and camera hardware identifiers entirely in-memory with zero disk persistence, providing an instant privacy-scrubbed download.
5. **JSON/CSV Profile Feed Ingestion:** Rule-based and keyword NLP scanner for synthetic/exported `profile.json` and `posts.json` files.
6. **Executive Cyber Telemetry Dashboard:** Responsive dark-mode dashboard with Chart.js radar charts, doughnut distributions, and threat finding breakdowns.
7. **Comprehensive Printable Privacy Report & Checklist:** Exportable executive summary with prioritized action steps.
8. **Synthetic Benchmark Dataset:** Includes a statistically calibrated dataset of 1,200 fictional user profiles.

---

## System Architecture

```
User Questionnaire / JSON Feed
              │
              ▼
   [ Input Validation Engine ]
              │
              ▼
   [ Privacy Feature Extraction ] ─── (Converts answers into 0-100 numerical risk features)
              │
              ▼
   [ Category Scoring Engine ] ────── (Computes 10 category scores via normalized weights)
              │
              ▼
   [ Overall Risk Engine ] ────────── (Calculates composite 0-100 score & risk tier)
              │
      ┌───────┴───────┐
      ▼               ▼
[ Findings ]    [ Recommendations ]
      │               │
      └───────┬───────┘
              ▼
   [ Improvement Simulator ] ──────── (Interactive "What-If" delta recalculation)
              │
              ▼
 [ Privacy by Design SQLite Store ] ─ (Stores scores & finding IDs only; zero PII)
              │
              ▼
 [ Responsive Frontend Dashboard ]
```

---

## Technology Stack

- **Backend:** Python 3.10+ / FastAPI (REST API with automatic OpenAPI documentation at `/docs`).
- **Data Validation:** Pydantic v2 (strict type enforcement and sanitization).
- **Database:** SQLite (anonymized, data-minimized relational storage).
- **Image Processing:** Pillow / PIL (local in-memory EXIF extraction and stripping).
- **Frontend:** Vanilla HTML5, CSS3 (modern slate cybersecurity theme), ES6 JavaScript.
- **Data Visualization:** Chart.js (interactive radar and doughnut charts).
- **Testing:** Pytest (32 automated unit and integration tests).

---

## The 45-Question Assessment & 10 Risk Categories

The questionnaire evaluates 45 granular indicators across 10 weighted categories:

1. **Profile Visibility (10%):** Search engine indexing, profile discoverability via phone/email, public follower lists.
2. **Personal Information Exposure (15%):** Public phone numbers, email addresses, full birth years, and residential locations.
3. **Location Privacy (15%):** Real-time check-ins, travel plan broadcasting, daily jog/commute routines, photo geotagging.
4. **Posts & Content (10%):** Public default timeline posts, employee ID badges, workstation screens, boarding passes, minor identification.
5. **Friends & Followers (10%):** Unvetted connection requests, lack of contact pruning, participation in follower pods.
6. **Tagging & Mentions (5%):** Timeline review queues, unrestricted photo tagging, unsolicited handle mentions.
7. **Authentication & Account Security (15%):** MFA usage, password reuse, unrecognized login alerts, stale session hygiene.
8. **Third-Party Apps (5%):** Stale OAuth tokens, viral quiz permissions, direct message scope grants.
9. **Messaging & Social Engineering (10%):** OTP code confidentiality, DM phishing awareness, viral biographical trivia quizzes.
10. **Digital Footprint (5%):** Legacy post archival, unattended zombie accounts, global handle reuse, self-OSINT audits.

---

## Risk Scoring Engine & Rubric

The overall Privacy Risk Score ($S$) is calculated using normalized category weights:
$$S = \min\left(100, \sum_{i=1}^{10} w_i \cdot C_i\right)$$

### Risk Classifications
- **0–20 (LOW):** Minimal exposure; strong privacy controls and authentication defense.
- **21–40 (MODERATE):** Typical exposure; minor PII or configuration adjustments recommended.
- **41–70 (HIGH):** Substantial exposure; public contact identifiers, disabled MFA, or travel disclosures.
- **71–100 (CRITICAL):** Severe attack surface; exposed phone number, no MFA, real-time location check-ins.

---

## Privacy Improvement Simulator

The framework features an interactive "What-If" simulator:
- **Baseline Scenario:** Initial score: **72/100 (CRITICAL)**.
- **Simulated Hardening:** User checks:
  - *Make phone number private*
  - *Disable real-time location check-ins*
  - *Enable Multi-Factor Authentication*
  - *Enable Timeline Tag Review*
- **Simulated Outcome:** Hardened score: **34/100 (MODERATE)**.
- **Demonstrated Impact:** **38 points risk reduction (52.8% decrease)** with specific resolved threat weaknesses listed!

---

## Photo EXIF Metadata Inspector & Scrubber

Smartphone cameras routinely embed hidden EXIF metadata into photos, including camera serial numbers, capture timestamps, and precise **GPS latitude/longitude coordinates**.
- **Local & In-Memory:** Images uploaded to the `/metadata` page are processed entirely in RAM.
- **Zero Storage:** Images are never written to permanent disk or sent to third-party APIs.
- **Sanitizer:** Users can click **"Strip Metadata & Download Clean Image"** to generate sanitized, safe-to-post copies.

---

## Privacy by Design & Safe Storage

The database architecture adheres to strict data minimization principles:
- **Stored Data:** `assessment_id`, `created_at` timestamp, `overall_score`, `risk_level`, category numerical scores, finding identifiers.
- **Never Stored:** Passwords, real phone numbers, real emails, home addresses, private messages, or raw photos.
- **Right to Erasure:** Complete deletion supported via `DELETE /api/assessment/{id}`.

---

## Installation & Local Execution

### Prerequisites
- Python 3.10+ installed on your system.

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/Social-Media-Privacy-Risk-Assessment.git
cd Social-Media-Privacy-Risk-Assessment
```

### Step 2: Create and Activate Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Generate Synthetic Dataset
```bash
python data/generate_dataset.py
```

### Step 5: Start the Application
```bash
python run.py
```

### Step 6: Open in Browser
- **Home Page:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Privacy Assessment:** [http://127.0.0.1:8000/assessment](http://127.0.0.1:8000/assessment)
- **Risk Dashboard:** [http://127.0.0.1:8000/dashboard](http://127.0.0.1:8000/dashboard)
- **EXIF Inspector:** [http://127.0.0.1:8000/metadata](http://127.0.0.1:8000/metadata)
- **Interactive REST API Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## REST API Documentation

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/questions` | Retrieves all 45 diagnostic questions and 10 categories. |
| `POST` | `/api/assessment` | Evaluates answers, calculates scores, and returns findings. |
| `GET` | `/api/assessment/{id}` | Retrieves a saved assessment record by ID. |
| `GET` | `/api/assessment/{id}/recommendations` | Retrieves prioritized remediation actions for an assessment. |
| `POST` | `/api/assessment/simulate-improvement` | Recalculates risk reduction based on proposed setting fixes. |
| `DELETE` | `/api/assessment/{id}` | Permanently deletes an assessment (Right to Erasure). |
| `GET` | `/api/dashboard/stats` | Retrieves aggregate metrics and risk distribution telemetry. |
| `GET` | `/api/privacy-checklist` | Returns structured privacy checklist items. |
| `POST` | `/api/analyze-json` | Evaluates synthetic `profile.json` and `posts.json` feeds. |
| `POST` | `/api/metadata/inspect` | In-memory EXIF extraction of uploaded image. |
| `POST` | `/api/metadata/strip` | Strips EXIF metadata and returns sanitized image stream. |

---

## Automated Testing Suite (32 Tests)

Run the automated test suite with pytest:
```bash
python -m pytest -v tests/test_privacy_framework.py
```

### Test Coverage Highlights:
- ✅ Baseline tests for fully private (score < 15, LOW) and fully public (score > 85, CRITICAL) profiles.
- ✅ Granular tests for public phone, email, birthday, location, travel, and workplace exposures.
- ✅ Boundary condition verification for score thresholds (20, 40, 70).
- ✅ Prioritization validation for immediate vs. good practice recommendations.
- ✅ Mathematical delta verification for the improvement simulator.
- ✅ **Security & Privacy Audit:** Verifies database schema strictly contains zero forbidden columns (`password`, `phone`, `email`, `address`, `ssn`).

---

## Documentation & Proof of Work Artifacts

Comprehensive documentation is provided in the `docs/` folder:
- [Threat Model](docs/THREAT_MODEL.md): Asset identification, exposure channels, likelihood/impact matrix.
- [Project Report](docs/PROJECT_REPORT.md): Academic course project report with full methodology and results.
- [Privacy Checklist](docs/PRIVACY_CHECKLIST.md): Printable 18-point hardening checklist.
- [Social Engineering Awareness](docs/SOCIAL_ENGINEERING_AWARENESS.md): Defensive guide on OSINT weaponization.
- [Interview Preparation Guide](docs/INTERVIEW_PREP.md): 10 predicted interview questions with in-depth model answers.
- [Resume & LinkedIn Guide](docs/RESUME_LINKEDIN_GUIDE.md): Tailored resume bullet points and LinkedIn announcement template.

---

## License & Author

- **Author:** Cybersecurity Student Researcher
- **Course:** Information Security & Privacy Engineering
- **License:** [MIT License](LICENSE) — Open for educational and non-commercial defensive security research.
