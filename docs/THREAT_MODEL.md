# Threat Model: Social Media Privacy & Personal Threat Surface

## 1. Overview
This threat model assesses the attack vectors, exposure categories, and risk likelihood for a standard social media user or enterprise employee operating public or semi-public social media accounts.

---

## 2. Asset Identification

| Asset ID | Asset Name | Description | Sensitivity |
| :--- | :--- | :--- | :--- |
| **A-01** | Account Access & Sessions | Authentication credentials, active login tokens, and recovery channels. | **CRITICAL** |
| **A-02** | Identity & Biographical Data | Full legal name, date of birth, mother's maiden name, family links, national IDs. | **CRITICAL** |
| **A-03** | Contact Details | Personal phone numbers, primary email addresses, and recovery phone numbers. | **HIGH** |
| **A-04** | Physical Location & Movements | Current physical location, home address, daily commute routes, vacation timelines. | **HIGH** |
| **A-05** | Private Content & Messages | Direct messages, non-public photos, confidential shared media, unlisted posts. | **HIGH** |
| **A-06** | Social & Professional Ties | Workplace roles, internal organizational hierarchies, family links, friends list. | **MEDIUM** |

---

## 3. Threat Identification & Risk Matrix

| Threat ID | Targeted Asset | Threat Description | Likelihood | Impact | Overall Risk | Existing Control | Recommended Defensive Control |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **T-01** | A-01 | **Account Takeover via Credential Stuffing:** Reusing passwords exposed in external breaches. | HIGH | CRITICAL | **CRITICAL** | Basic password | Unique password via Password Manager + App-based MFA (TOTP). |
| **T-02** | A-03 | **SIM Swapping & Smishing:** Public mobile numbers harvested for carrier port-out or SMS phishing. | MEDIUM | CRITICAL | **CRITICAL** | SMS-based MFA | Remove phone from bio; switch 2FA to hardware tokens / TOTP apps. |
| **T-03** | A-04 | **Opportunistic Burglary / Stalking:** Real-time check-ins and travel itinerary posts revealing empty homes. | MEDIUM | HIGH | **HIGH** | Post-deletion | Delay posting vacation photos until after returning home safely. |
| **T-04** | A-02, A-06 | **Targeted Spear Phishing / Pretexting:** Attacker leverages workplace badges and family ties to craft urgent lures. | HIGH | HIGH | **HIGH** | Spam filters | Omit badges, desk displays, and internal organization hierarchies from posts. |
| **T-05** | A-04 | **EXIF Metadata Geolocation:** Image uploads leaking precise GPS coordinates of private residences. | MEDIUM | HIGH | **HIGH** | Platform compression | Disable camera GPS permissions; sanitize EXIF metadata before sharing. |
| **T-06** | A-01, A-05 | **Malicious Third-Party OAuth Access:** Stale quiz or analytics apps abusing persistent read/write scopes. | MEDIUM | MEDIUM | **MEDIUM** | Platform review | Quarterly audit of connected apps; enforce principle of least privilege. |
| **T-07** | A-02 | **OSINT Biographical Harvesting:** Interactive trivia quizzes harvesting security question answers. | HIGH | MEDIUM | **MEDIUM** | None | Refrain from viral trivia quizzes; use randomized answers for security questions. |
| **T-08** | A-05 | **Unfiltered External Tagging:** Malicious accounts tagging users in cryptocurrency scams or inappropriate photos. | HIGH | MEDIUM | **MEDIUM** | Manual untagging | Enable Timeline / Tag Review approval queue across all platforms. |

---

## 4. Mitigation Strategy & Defense-in-Depth
1. **Perimeter Hardening:** Set profiles to Friends-only and disable search engine indexing.
2. **Access Control:** Enforce multi-factor authentication and purge stale sessions.
3. **Data Minimization:** Keep phone numbers, full birth dates, and residential addresses off public profiles.
4. **Behavioral Discipline:** Practice time-delayed posting for travel memories and reject unverified connections.
