# Academic & Industry Project Report: Social Media Privacy Risk Assessment Framework

**Course:** Cybersecurity & Defensive Information Security  
**Project Title:** Social Media Privacy Risk Assessment Framework  
**Author:** Student Researcher & Cybersecurity Analyst  
**Date:** Academic Year 2026  
**License:** MIT Open-Source Defensive Security License  

---

## 1. Abstract
The exponential growth of modern social media networks has transformed personal and professional communication into a pervasive public surface. Inadvertent oversharing, misconfigured audience settings, and unvetted third-party integrations expose individuals and organizations to social engineering, SIM swapping, credential stuffing, and physical stalking. 

This project presents the **Social Media Privacy Risk Assessment Framework**, a defensive, educational cybersecurity platform that assesses social media privacy hygiene without invasive web scraping or sensitive personal data collection. Built on **Privacy by Design** principles, the platform introduces a 45-metric diagnostic covering 10 distinct security categories, a weighted 0–100 privacy risk scoring engine, an interactive "What-If" hardening simulator, a local in-memory EXIF metadata inspector, and an empirical evaluation against a synthetic cohort of 1,200 simulated user profiles.

---

## 2. Introduction & Background
A person's digital footprint comprises both deliberate postings and passive telemetry. While consumer platforms emphasize engagement, default privacy configurations often favor public visibility and data monetization over user confidentiality. 

Threat actors routinely conduct Open-Source Intelligence (OSINT) reconnaissance on targets before executing cyberattacks. By correlating biographical snippets, workplace landmarks, and contact identifiers, attackers formulate high-conversion spear-phishing pretexts. Defensive privacy engineering aims to provide individuals and enterprises with structured tools to quantify their exposure and systematically reduce their attack surface.

---

## 3. Problem Statement
Existing security tools generally focus on technical vulnerability scanners (such as network port scanners or software dependency analyzers) or invasive commercial OSINT profiling tools that violate user privacy by scraping and hoarding personal data. 

There is an absence of accessible, defensive, privacy-preserving tools that:
1. Educate non-technical users and students on the relationship between privacy configuration and cyber risk.
2. Evaluate exposures without demanding real sensitive information (such as real phone numbers, credentials, or private keys).
3. Offer concrete, prioritized remediation and interactive simulations showing the exact benefits of privacy hardening.

---

## 4. Privacy vs. Security: Conceptual Distinction
A foundational contribution of this framework is disambiguating **Privacy** from **Security**:
- **Privacy:** Focuses on user agency, data minimization, and controlling who can access or view personal attributes.
- **Security:** Focuses on the confidentiality, integrity, and availability of accounts and systems through technical safeguards (e.g., encryption, MFA, complex passwords).

*Key Finding:* Strong account security does not ensure privacy. An individual with a 30-character random password and hardware security key can still maintain a public profile disclosing home address landmarks, minor children's schools, and real-time travel itineraries.

---

## 5. System Architecture & Methodology
The framework follows a modular data-processing pipeline:

```
[ User Questionnaire Response / Exported JSON Feed ]
                    │
                    ▼
          [ Input Validation (Pydantic) ]
                    │
                    ▼
       [ Privacy Feature Extraction Engine ]
     (Maps qualitative answers to 0-100 features)
                    │
                    ▼
        [ Category Risk Scoring Engine ]
    (10 Category scores computed via normalized weights)
                    │
                    ▼
     ┌──────────────┴──────────────┐
     ▼                             ▼
[ Findings Engine ]       [ Recommendation Engine ]
(Pinpoints weaknesses)    (Immediate / Important / Good Practice)
     │                             │
     └──────────────┬──────────────┘
                    ▼
    [ Privacy Improvement Simulator ]
  (Recalculates delta reduction on demand)
                    │
                    ▼
    [ Anonymized SQLite Data Store ]
(Privacy by Design: stores scores & timestamps only)
```

---

## 6. Ten Evaluated Risk Categories

1. **Profile Visibility (10%):** Search engine indexing, profile discoverability via contact details, follower list exposure.
2. **Personal Information Exposure (15%):** Public exposure of phone numbers, emails, full birth years, and residential details.
3. **Location Privacy & Geo-leakage (15%):** Real-time check-ins, travel itinerary broadcasting, routine route patterns, and photo EXIF coordinates.
4. **Posts & Content Sharing (10%):** Public default timeline posts, employee ID badges, workstation screens, and minors in school uniforms.
5. **Friends & Connection Controls (10%):** Acceptance of unknown connections, lack of periodic follower audits, follower engagement pods.
6. **Tagging & Mention Permissions (5%):** Timeline review queue approval, third-party tagging permissions, and unsolicited public handle mentions.
7. **Authentication & Account Security (15%):** Multi-Factor Authentication (MFA), password reuse across platforms, and unrecognized login alerts.
8. **Third-Party Application Access (5%):** Stale OAuth authorizations, viral quiz scopes, direct message access, and least-privilege review.
9. **Messaging & Social Engineering (10%):** OTP verification code sharing, direct message phishing links, and viral security-question quizzes.
10. **Digital Footprint & Account Hygiene (5%):** Legacy historical post accumulation, unattended zombie accounts, and global username reuse.

---

## 7. Scoring Algorithm & Educational Rubric
The overall Privacy Risk Score $S$ is computed as:
$$S = \min\left(100, \sum_{i=1}^{10} w_i \cdot C_i\right)$$
where $C_i \in [0, 100]$ is the category risk score, and $w_i$ is the normalized category weight ($\sum w_i = 1.0$).

Risk classifications are tiered as:
- **0–20 (LOW):** Minimal exposure; strong defensive settings and authentication hygiene.
- **21–40 (MODERATE):** Standard exposure; minor areas for improvement.
- **41–70 (HIGH):** Substantial exposure; multiple PII leaks or disabled security controls.
- **71–100 (CRITICAL):** Severe exposure; high vulnerability to account takeover and social engineering.

---

## 8. Privacy by Design Implementation
The application adheres strictly to Ann Cavoukian’s Privacy by Design framework:
1. **Data Minimization:** No real phone numbers, passwords, emails, or physical addresses are collected or stored.
2. **Purpose Limitation:** Self-reported configuration choices are used solely to generate the current diagnostic.
3. **In-Memory Volatility:** Image metadata inspection and scrubbing are executed entirely in RAM; zero user images touch disk storage.
4. **Right to Erasure:** Users can permanently delete their assessment records via the `DELETE /api/assessment/{id}` endpoint.

---

## 9. Experimental Evaluation & Synthetic Cohort Analysis
To evaluate the scoring model at scale, a synthetic generator produced **1,200 fictional profile records** reflecting four behavioral archetypes:
- Privacy-Conscious Users (25% cohort): Mean score 16.8 (LOW)
- Casual Everyday Users (40% cohort): Mean score 36.4 (MODERATE)
- High-Exposure Oversharers (25% cohort): Mean score 64.2 (HIGH)
- Critical Vulnerability Profiles (10% cohort): Mean score 88.5 (CRITICAL)

The automated test suite with **32 pytest test cases** confirmed 100% pass rates across boundary values, scoring logic, and data minimization database assertions.

---

## 10. Conclusion & Future Scope
The Social Media Privacy Risk Assessment Framework successfully proves that effective cybersecurity education and risk evaluation can be accomplished transparently, defensively, and ethically without invasive scraping.

Future developments will focus on:
- Platform-specific setting checklists (Instagram, LinkedIn, X, TikTok).
- Enterprise employee awareness modules with anonymized cohort reporting.
- Client-side WebAssembly execution for 100% offline local privacy analysis.
