# Technical Interview Preparation Guide: 10 Core Questions & In-Depth Answers

This guide prepares you to speak confidently in cybersecurity, GRC, SOC, and privacy engineering job interviews about the architecture, implementation, and ethics of your project.

---

### Question 1: Explain your project.
**Answer:**
> "I designed and built the **Social Media Privacy Risk Assessment Framework**, an industry-oriented defensive cybersecurity project that evaluates a user's social media privacy and exposure risks without scraping real accounts or collecting sensitive data. 
> 
> The application guides users through a structured 45-question diagnostic covering ten categories—such as personal information exposure, location privacy, authentication hygiene, third-party OAuth access, tagging controls, and social-engineering resilience. 
> 
> Behind the scenes, the framework converts these responses into numerical risk feature vectors and computes category scores and an overall privacy risk score from 0 to 100, where higher scores represent higher risk. It pinpoints specific vulnerabilities, issues prioritized recommendations, and features an interactive **Privacy Improvement Simulator** that demonstrates how applying defensive hardening reduces exposure.
> 
> The platform also includes a safe local image EXIF metadata inspector and scrubber, runs on FastAPI and SQLite, and strictly follows Privacy by Design principles by storing only anonymized scores and finding identifiers."

---

### Question 2: What is the fundamental difference between privacy and security?
**Answer:**
> "Privacy and security are closely related but distinct disciplines:
> - **Privacy** governs how personal information is collected, exposed, shared, and utilized. It focuses on user consent, data minimization, and audience boundaries.
> - **Security** focuses on protecting systems, data, and accounts from unauthorized access, modification, or destruction. It relies on controls like encryption, multi-factor authentication, and access control lists.
> 
> The critical insight in my project is that **Strong Account Security does not equal Strong Privacy**. A user could have a 25-character random password and hardware-token MFA—meaning their account is highly secure against credential stuffing—yet they might publicly post their personal phone number, full birth year, and live vacation check-ins. Their account security is solid, but their privacy risk is critical."

---

### Question 3: What is a digital footprint, and how does your framework evaluate it?
**Answer:**
> "A digital footprint is the cumulative trail of data left behind by a person’s online activity. It consists of:
> 1. **Active Footprint:** Data deliberately shared, such as posts, photos, comments, and profile details.
> 2. **Passive Footprint:** Data collected unobtrusively, such as IP logs, browser fingerprints, and activity timestamps.
> 
> In my framework, I deliberately evaluate only self-reported active practices and account hygiene—such as whether users audit old posts from years ago, delete forgotten 'zombie' accounts, manage bio link aggregators, and search their own name to monitor OSINT exposure. I do not track users or scrape real accounts, which ensures the evaluation remains purely defensive and privacy-preserving."

---

### Question 4: How does your privacy risk scoring algorithm work?
**Answer:**
> "The scoring engine utilizes a transparent, weighted multi-tier rubric:
> 1. Each of the 45 questions maps user answers to a 0–100 risk feature (e.g., public phone = 100, private = 0).
> 2. Questions are aggregated across 10 distinct security categories to produce category-level scores (0–100).
> 3. The overall score is calculated as a normalized weighted sum of the category scores using configurable weights—for instance, 15% for personal information, 15% for location, 15% for account security, down to 5% for tagging and digital footprint.
> 4. The overall score maps into four clear risk tiers: Low (0–20), Moderate (21–40), High (41–70), and Critical (71–100).
> 
> I always emphasize that these weights and thresholds are educational assumptions designed for risk coaching, and would be formally calibrated against organizational policies in an enterprise deployment."

---

### Question 5: How does social media oversharing increase social engineering and cybersecurity risk?
**Answer:**
> "Social engineering relies heavily on psychological manipulation and establishing believable pretexts. When users overshare on social media, threat actors harvest contextual intelligence for free via OSINT:
> - Sharing photos of new employee badges provides internal company IDs, formats, and building numbers.
> - Announcing upcoming travel reveals when a physical residence is empty and enables urgent family emergency wire scams.
> - Participating in viral trivia games ('What was your first car?') leaks answers to account recovery security questions.
> 
> Publicly exposed biographical context makes phishing emails, smishing messages, and executive impersonation significantly more convincing."

---

### Question 6: Why did you include Multi-Factor Authentication (MFA) in a privacy project?
**Answer:**
> "Account security and privacy are deeply intertwined in the threat lifecycle. If an adversary takes over a social media account via credential stuffing or password reuse, they instantly gain unauthorized access to all private direct messages, confidential photos, private stories, and contacts list. 
> 
> Therefore, account takeover represents an instantaneous and catastrophic privacy breach. Including MFA evaluates whether the user has implemented defense-in-depth to protect their private communications from being exposed."

---

### Question 7: What privacy risks do third-party OAuth applications create?
**Answer:**
> "Many users authorize third-party apps—such as personality quizzes, games, or analytics tools—using 'Sign in with Social Account'. These authorizations grant persistent OAuth tokens with scopes that may include reading profile details, friend lists, or even direct messages.
> 
> Over time, users forget about these apps, yet the access tokens remain valid indefinitely. If the third-party developer's database is subsequently breached, the attacker can leverage those stale tokens to access user data. My framework evaluates whether users regularly audit connected apps and applies the **Principle of Least Privilege** by recommending revoking unnecessary integrations."

---

### Question 8: What is Privacy by Design, and how did you implement it in code?
**Answer:**
> "Privacy by Design, formulated by Ann Cavoukian, means embedding privacy proactive controls into IT architecture from the outset rather than bolting them on afterward. In my project, I applied:
> 1. **Data Minimization:** I never ask users to enter their actual phone number, email, birth date, or address. I only ask binary/categorical configuration questions (*'Is your phone number publicly visible? YES/NO'*).
> 2. **Zero Sensitive Storage:** The SQLite database stores only the assessment ID, timestamp, numerical category scores, and finding identifiers. No credentials or personal identifiers are stored.
> 3. **In-Memory Image Processing:** The EXIF metadata inspector parses uploaded photos in memory and strips EXIF tags without ever saving files to permanent disk storage.
> 4. **User Control / Right to Erasure:** I implemented a `DELETE /api/assessment/{id}` endpoint to allow users to permanently purge their assessment record."

---

### Question 9: What is the Privacy Improvement Simulator and why is it valuable?
**Answer:**
> "The Privacy Improvement Simulator is an interactive 'What-If' feature. After receiving an initial risk score (for example, 72/100, Critical), the user can toggle checkboxes representing recommended hardening actions—such as making their phone number private, enabling MFA, disabling real-time location check-ins, and turning on tag review.
> 
> When they click simulate, the backend dynamically merges these changes, re-runs the feature extraction and scoring engines, and displays the new score (e.g., 34/100, Moderate) alongside the delta reduction (e.g., 38 points reduced) and a list of resolved weaknesses. 
> 
> This provides immediate positive reinforcement and shows users that privacy is actionable rather than overwhelming."

---

### Question 10: How did you test your application, and what would you build next?
**Answer:**
> "I wrote a comprehensive automated test suite with **32 pytest tests** verifying:
> - Fully private versus fully public profile score baselines.
> - Individual vulnerability contributions and boundary conditions (20, 40, 70).
> - Security and privacy schema audits ensuring no forbidden PII columns exist in SQLite.
> - End-to-end REST API request-response contracts and JSON feed parsing.
> 
> For future improvements, I would build platform-specific privacy setting step-by-step guides (tailored for Instagram, LinkedIn, and X), introduce configurable enterprise compliance profiles (like HIPAA or FERPA for schools and clinics), and develop a local client-side WebAssembly mode where assessment processing never leaves the user's browser."
