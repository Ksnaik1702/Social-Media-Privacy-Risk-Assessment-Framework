# Social Engineering Awareness: How Oversharing Fuels Cyberattacks

## 1. Executive Summary
Social engineering is the psychological manipulation of people into performing actions or divulging confidential information. Threat actors rarely attack technical encryption directly when human context can be harvested for free through social media oversharing.

This guide provides defensive cybersecurity awareness explaining how threat actors weaponize publicly available context without providing offensive attack scripts.

---

## 2. The OSINT Weaponization Lifecycle
In an Open-Source Intelligence (OSINT) attack cycle, attackers collect disparate breadcrumbs to construct a believable **pretext**:

```
[ Public Social Post ]  -->  [ Context Extraction ]  -->  [ Pretext Formulation ]  -->  [ Targeted Exploitation ]
e.g. "Excited to join         Identifies Employer,        Poses as internal IT         Victim surrenders SSO
     Acme as Cloud Eng!"      Role, and Start Date        support during onboarding    credentials or OTP token
```

---

## 3. High-Risk Exposure Vectors and Threat Mechanics

### A. Workplace Badging & Corporate ID Photos
- **The Overshare:** Uploading high-resolution photos of newly issued employee badges, lanyard cards, or company laptops.
- **The Threat:** 
  1. Barcodes and QR codes on badges can be decoded to extract internal Employee ID numbers.
  2. Logo placement, lanyard colors, and building numbers assist physical penetration testers and unauthorized infiltrators.
  3. Attackers use employee names and roles to launch Business Email Compromise (BEC) and executive impersonation scams.

### B. Travel Plans & Real-Time Itineraries
- **The Overshare:** Posting boarding passes, airport check-ins ("En route to Paris for 2 weeks!"), or hotel room views.
- **The Threat:**
  1. Boarding pass barcodes contain Passenger Name Records (PNR) and frequent flyer numbers, allowing unauthorized flight cancellations or seat reassignments.
  2. Broadcasting absence from home signals an unoccupied residence to local opportunistic burglars.
  3. Pretexting calls targeting family members ("Your child was in an accident while abroad in Paris, wire emergency funds") become distressingly plausible.

### C. Biographical Quizzes & Nostalgia Games
- **The Overshare:** Commenting on viral engagement posts: *"What was your first car? Your mother's maiden name? The street you grew up on?"*
- **The Threat:** These questions map directly to common banking and account recovery security questions. Attackers aggregate responses across engagement threads to reset account credentials.

### D. Verification Code (OTP) Solicitations
- **The Overshare:** Responding to urgent direct messages from a mutual friend: *"Hey, my phone is locked, I asked Instagram to send my backup code to your phone, can you tell me the 6 digits?"*
- **The Threat:** The friend's account has been compromised. The attacker actually entered the victim's phone number into a password reset portal; the 6 digits will transfer ownership of the victim's account to the adversary.

---

## 4. Defensive Rules of Engagement
1. **Never Disclose Authentication Codes:** Platforms never ask users to transmit OTP codes over chat or phone.
2. **Implement Out-of-Band Verification:** If a colleague or friend messages requesting emergency financial aid or gift cards, verify via a trusted direct phone call.
3. **Practice Delayed Sharing:** Share vacation memories, concert photos, and restaurant experiences only after departing the venue.
4. **Scrub Credentials and Physical Tokens:** Never photograph car keys (which can be cut from high-resolution images), credit cards, boarding passes, or office desk displays.
