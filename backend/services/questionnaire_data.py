"""
Privacy Assessment Questionnaire Data
Comprehensive 45-question diagnostic across 10 security & privacy categories.
Designed to assess posture without asking for actual sensitive personal information.
"""

CATEGORIES = {
    "profile_visibility": {
        "id": "profile_visibility",
        "name": "Profile Visibility",
        "description": "Evaluates public discoverability, search indexation, and profile accessibility.",
        "weight": 0.10
    },
    "personal_information": {
        "id": "personal_information",
        "name": "Personal Information Exposure",
        "description": "Evaluates public exposure of identity-linked attributes (DOB, phone, email, bio).",
        "weight": 0.15
    },
    "location_privacy": {
        "id": "location_privacy",
        "name": "Location Privacy & Geo-leakage",
        "description": "Assesses real-time geotagging, travel plan broadcasting, and routine disclosures.",
        "weight": 0.15
    },
    "posts_content": {
        "id": "posts_content",
        "name": "Posts & Content Sharing",
        "description": "Evaluates default audience controls, sensitive workplace/school posts, and media exposure.",
        "weight": 0.10
    },
    "friends_followers": {
        "id": "friends_followers",
        "name": "Friends & Connection Controls",
        "description": "Reviews connection vetting, friend list exposure, and unknown follower acceptance.",
        "weight": 0.10
    },
    "tagging_mentions": {
        "id": "tagging_mentions",
        "name": "Tagging & Mention Permissions",
        "description": "Analyzes external tagging policies, post review queues, and automatic timeline additions.",
        "weight": 0.05
    },
    "account_security": {
        "id": "account_security",
        "name": "Authentication & Account Security",
        "description": "Examines MFA usage, password management, login alerts, and active session hygiene.",
        "weight": 0.15
    },
    "third_party_apps": {
        "id": "third_party_apps",
        "name": "Third-Party Application Access",
        "description": "Assesses OAuth authorizations, stale integrations, and least privilege application access.",
        "weight": 0.05
    },
    "social_engineering": {
        "id": "social_engineering",
        "name": "Messaging & Social Engineering",
        "description": "Evaluates awareness of impersonation, suspicious links, verification code requests, and scams.",
        "weight": 0.10
    },
    "digital_footprint": {
        "id": "digital_footprint",
        "name": "Digital Footprint & Account Hygiene",
        "description": "Reviews legacy posts, unused accounts, public search history, and recurring audits.",
        "weight": 0.05
    }
}

QUESTIONS = [
    # ==========================================
    # CATEGORY A: Profile Visibility (Questions 1-4)
    # ==========================================
    {
        "id": "q_pv_1",
        "category_id": "profile_visibility",
        "question": "What is the general visibility setting of your primary social media profile?",
        "options": ["PUBLIC", "FRIENDS", "PRIVATE"],
        "risk_mapping": {"PUBLIC": 100, "FRIENDS": 30, "PRIVATE": 0},
        "explanation": "A public profile allows anyone on the internet, including automated scrapers, to inspect your bio and profile details.",
        "remediation": "Switch profile visibility to Friends-only or Private unless public exposure is strictly necessary for professional branding.",
        "severity": "HIGH",
        "finding_title": "Profile is publicly accessible"
    },
    {
        "id": "q_pv_2",
        "category_id": "profile_visibility",
        "question": "Can external search engines (such as Google or Bing) index your profile page?",
        "options": ["YES", "NO", "NOT_SURE"],
        "risk_mapping": {"YES": 100, "NOT_SURE": 60, "NO": 0},
        "explanation": "Search engine indexation permanently preserves cached copies of your profile and makes you easily discoverable in OSINT lookups.",
        "remediation": "Disable 'Allow search engines outside this platform to link to your profile' in privacy settings.",
        "severity": "MEDIUM",
        "finding_title": "Search engine indexing enabled"
    },
    {
        "id": "q_pv_3",
        "category_id": "profile_visibility",
        "question": "Can people find your profile by searching your phone number or email address?",
        "options": ["YES", "NO", "NOT_SURE"],
        "risk_mapping": {"YES": 90, "NOT_SURE": 50, "NO": 0},
        "explanation": "Lookup discoverability allows adversaries with a leaked phone number or email from a breach to map your identity to your profile.",
        "remediation": "Restrict account lookup by email/phone to 'Nobody' or 'Friends only'.",
        "severity": "HIGH",
        "finding_title": "Profile discoverable via contact identifiers"
    },
    {
        "id": "q_pv_4",
        "category_id": "profile_visibility",
        "question": "Is your followers or friends list visible to anyone other than your approved connections?",
        "options": ["PUBLIC", "FRIENDS", "PRIVATE"],
        "risk_mapping": {"PUBLIC": 80, "FRIENDS": 20, "PRIVATE": 0},
        "explanation": "Public friends lists facilitate relationship mapping, spear phishing of close contacts, and impersonation schemes.",
        "remediation": "Set follower/friend list visibility to 'Only Me' or 'Mutual connections'.",
        "severity": "MEDIUM",
        "finding_title": "Publicly exposed connections list"
    },

    # ==========================================
    # CATEGORY B: Personal Information (Questions 5-9)
    # ==========================================
    {
        "id": "q_pi_1",
        "category_id": "personal_information",
        "question": "Is your phone number displayed or visible on your public bio/profile?",
        "options": ["YES", "NO"],
        "risk_mapping": {"YES": 100, "NO": 0},
        "explanation": "Public phone numbers expose users to SIM swapping, smishing (SMS phishing), spam caller harvesting, and credential recovery resets.",
        "remediation": "Remove phone numbers from public view; use masked contact forms or separate disposable communication channels.",
        "severity": "CRITICAL",
        "finding_title": "Phone number publicly exposed"
    },
    {
        "id": "q_pi_2",
        "category_id": "personal_information",
        "question": "Is your personal email address displayed on your bio or public profile?",
        "options": ["YES", "NO"],
        "risk_mapping": {"YES": 90, "NO": 0},
        "explanation": "Direct public email listings are targeted by spam bots, phishing campaigns, and brute-force credential stuffing lists.",
        "remediation": "Hide personal email address; if business inquiries are required, use a dedicated alias or privacy-relay email.",
        "severity": "HIGH",
        "finding_title": "Personal email visible in profile"
    },
    {
        "id": "q_pi_3",
        "category_id": "personal_information",
        "question": "Is your full birth date (month, day, and birth year) publicly visible?",
        "options": ["YES", "NO", "SOMETIMES"],
        "risk_mapping": {"YES": 100, "SOMETIMES": 60, "NO": 0},
        "explanation": "Full birth dates are critical verification tokens used in identity theft, security question resets, and financial account verification.",
        "remediation": "Configure birth date visibility to hide the year completely or set the entire date to 'Only Me'.",
        "severity": "CRITICAL",
        "finding_title": "Full birth date publicly exposed"
    },
    {
        "id": "q_pi_4",
        "category_id": "personal_information",
        "question": "Do you publicly display your exact home city, street, or neighborhood?",
        "options": ["YES", "NO", "SOMETIMES"],
        "risk_mapping": {"YES": 85, "SOMETIMES": 45, "NO": 0},
        "explanation": "Localized residence exposure narrows down physical location and facilitates physical reconnaissance or targeted spear phishing.",
        "remediation": "Broaden location to state/country level or remove residential location completely.",
        "severity": "HIGH",
        "finding_title": "Residential neighborhood/city publicly shared"
    },
    {
        "id": "q_pi_5",
        "category_id": "personal_information",
        "question": "Do you list family members, children names, or relationship status publicly?",
        "options": ["YES", "NO", "SOMETIMES"],
        "risk_mapping": {"YES": 75, "SOMETIMES": 40, "NO": 0},
        "explanation": "Adversaries leverage family ties to craft believable urgent 'grandparent/family emergency' social engineering scams.",
        "remediation": "Remove family linkages from public profiles and keep relationship details private.",
        "severity": "MEDIUM",
        "finding_title": "Family and relationship data exposed"
    },

    # ==========================================
    # CATEGORY C: Location Privacy (Questions 10-14)
    # ==========================================
    {
        "id": "q_loc_1",
        "category_id": "location_privacy",
        "question": "Do you regularly post real-time location check-ins when visiting venues or events?",
        "options": ["YES", "SOMETIMES", "NO"],
        "risk_mapping": {"YES": 100, "SOMETIMES": 60, "NO": 0},
        "explanation": "Real-time check-ins broadcast your exact live physical whereabouts, exposing you to stalking and opportunistic burglaries.",
        "remediation": "Cease real-time check-ins; post photos and experiences only after departing the location.",
        "severity": "CRITICAL",
        "finding_title": "Real-time location check-ins enabled"
    },
    {
        "id": "q_loc_2",
        "category_id": "location_privacy",
        "question": "Do you post travel or vacation plans before or while you are away from home?",
        "options": ["YES", "SOMETIMES", "NO"],
        "risk_mapping": {"YES": 95, "SOMETIMES": 50, "NO": 0},
        "explanation": "Announcing empty homes during vacation windows is a primary signal exploited in residential property theft.",
        "remediation": "Share travel memories and trip photos only after returning home safely.",
        "severity": "HIGH",
        "finding_title": "Travel itineraries and empty-home periods broadcasted"
    },
    {
        "id": "q_loc_3",
        "category_id": "location_privacy",
        "question": "Does your camera or social app automatically attach GPS geotags to uploaded photos?",
        "options": ["YES", "NOT_SURE", "NO"],
        "risk_mapping": {"YES": 90, "NOT_SURE": 60, "NO": 0},
        "explanation": "Embedded GPS EXIF metadata in images can pinpoint precise coordinates of residences, schools, or secluded routes.",
        "remediation": "Disable camera location permissions in mobile device settings and review photo EXIF settings.",
        "severity": "HIGH",
        "finding_title": "Automatic geotagging and EXIF coordinate leakage"
    },
    {
        "id": "q_loc_4",
        "category_id": "location_privacy",
        "question": "Do you regularly post daily routine activities (e.g., daily 7 AM jog route, gym hours, commute path)?",
        "options": ["YES", "SOMETIMES", "NO"],
        "risk_mapping": {"YES": 85, "SOMETIMES": 45, "NO": 0},
        "explanation": "Predictable routine disclosures allow bad actors to map recurring daily habits and anticipate your physical presence.",
        "remediation": "Vary post timing and avoid sharing repetitive schedule/route details publicly.",
        "severity": "MEDIUM",
        "finding_title": "Daily physical routine patterns exposed"
    },
    {
        "id": "q_loc_5",
        "category_id": "location_privacy",
        "question": "Do your posts expose identifiable house exteriors, street signs, or vehicle license plates?",
        "options": ["YES", "SOMETIMES", "NO"],
        "risk_mapping": {"YES": 80, "SOMETIMES": 40, "NO": 0},
        "explanation": "Visible street names, distinctive architecture, or registration plates enable automated geolocating via Google Street View.",
        "remediation": "Crop or blur background landmarks, house numbers, and vehicle plates prior to posting.",
        "severity": "MEDIUM",
        "finding_title": "Geolocatable residential landmarks and license plates in media"
    },

    # ==========================================
    # CATEGORY D: Posts & Content (Questions 15-18)
    # ==========================================
    {
        "id": "q_cnt_1",
        "category_id": "posts_content",
        "question": "What is the default audience setting for your regular timeline posts and stories?",
        "options": ["PUBLIC", "FRIENDS", "PRIVATE"],
        "risk_mapping": {"PUBLIC": 95, "FRIENDS": 25, "PRIVATE": 0},
        "explanation": "Public timeline posts allow total strangers to harvest life events, emotional states, and contextual hooks.",
        "remediation": "Switch default audience setting from 'Public' to 'Friends' or a customized close connections list.",
        "severity": "HIGH",
        "finding_title": "Default post audience set to Public"
    },
    {
        "id": "q_cnt_2",
        "category_id": "posts_content",
        "question": "Do you post photos showing workplace badges, office desk screens, security keys, or company ID cards?",
        "options": ["YES", "SOMETIMES", "NO"],
        "risk_mapping": {"YES": 100, "SOMETIMES": 55, "NO": 0},
        "explanation": "Employee badges reveal company logos, badge formats, employee IDs, and bar/QR codes easily replicated for physical intrusion.",
        "remediation": "Never photograph workplace badges, interior restricted zones, or workstation screens.",
        "severity": "CRITICAL",
        "finding_title": "Workplace badge or workstation credentials photographed"
    },
    {
        "id": "q_cnt_3",
        "category_id": "posts_content",
        "question": "Do you post photos or updates identifying minors, children, or their school uniforms/locations?",
        "options": ["YES", "SOMETIMES", "NO"],
        "risk_mapping": {"YES": 90, "SOMETIMES": 50, "NO": 0},
        "explanation": "Sharenting (oversharing child information) creates non-consensual digital footprints and safety vulnerabilities for minors.",
        "remediation": "Refrain from posting minors publicly, blur faces, and obscure school logos and uniform emblems.",
        "severity": "HIGH",
        "finding_title": "Minors and educational institutions identifiable in content"
    },
    {
        "id": "q_cnt_4",
        "category_id": "posts_content",
        "question": "Do you post photos showing newly received keys, credit cards, boarding passes, or diplomas?",
        "options": ["YES", "SOMETIMES", "NO"],
        "risk_mapping": {"YES": 95, "SOMETIMES": 45, "NO": 0},
        "explanation": "Boarding pass barcodes contain Passenger Name Records (PNR) that allow ticket hijacking; physical keys can be 3D printed from clear photos.",
        "remediation": "Keep all boarding passes, keys, tickets, and official certificates off social channels.",
        "severity": "HIGH",
        "finding_title": "High-risk physical tokens (boarding passes/keys/cards) shared"
    },

    # ==========================================
    # CATEGORY E: Friends & Followers (Questions 19-22)
    # ==========================================
    {
        "id": "q_frn_1",
        "category_id": "friends_followers",
        "question": "Do you accept friend or connection requests from people you do not personally know or cannot verify?",
        "options": ["YES", "SOMETIMES", "NO"],
        "risk_mapping": {"YES": 95, "SOMETIMES": 55, "NO": 0},
        "explanation": "Sock-puppet and catfish accounts use fake connection requests to bypass 'Friends-only' privacy shields and collect private data.",
        "remediation": "Strictly verify or reject connection requests from unverified or unknown individuals.",
        "severity": "HIGH",
        "finding_title": "Unvetted and unknown connection requests accepted"
    },
    {
        "id": "q_frn_2",
        "category_id": "friends_followers",
        "question": "Do you periodically audit your friends and followers list to remove inactive or unfamiliar accounts?",
        "options": ["YES", "SOMETIMES", "NO"],
        "risk_mapping": {"NO": 80, "SOMETIMES": 40, "YES": 0},
        "explanation": "Abandoned or compromised accounts on your friends list may be repurposed by attackers to surveil your private timeline.",
        "remediation": "Conduct a quarterly connection audit to prune unfamiliar or dormant contacts.",
        "severity": "MEDIUM",
        "finding_title": "No regular follower/friend list audits performed"
    },
    {
        "id": "q_frn_3",
        "category_id": "friends_followers",
        "question": "Can strangers view mutual friends or see when you interact on friends' private posts?",
        "options": ["YES", "NOT_SURE", "NO"],
        "risk_mapping": {"YES": 75, "NOT_SURE": 45, "NO": 0},
        "explanation": "Interaction trails give third-party observers insights into personal relationships, affinities, and sentiment.",
        "remediation": "Review activity visibility and restrict interaction sharing outside your circle.",
        "severity": "MEDIUM",
        "finding_title": "Social interaction and mutual friend visibility unconstrained"
    },
    {
        "id": "q_frn_4",
        "category_id": "friends_followers",
        "question": "Do you participate in public follow-for-follow groups or accept followers to artificially inflate follower counts?",
        "options": ["YES", "SOMETIMES", "NO"],
        "risk_mapping": {"YES": 85, "SOMETIMES": 40, "NO": 0},
        "explanation": "Follower schemes systematically inject malicious bots and botnet monitors into your audience.",
        "remediation": "Avoid engagement pods and follower exchange networks; prioritize authentic connections.",
        "severity": "MEDIUM",
        "finding_title": "Participation in follower engagement pods"
    },

    # ==========================================
    # CATEGORY F: Tagging & Mentions (Questions 23-26)
    # ==========================================
    {
        "id": "q_tag_1",
        "category_id": "tagging_mentions",
        "question": "Is tag review (timeline review) enabled so you must approve tagged posts before they appear on your profile?",
        "options": ["YES", "NO", "NOT_SURE"],
        "risk_mapping": {"NO": 95, "NOT_SURE": 60, "YES": 0},
        "explanation": "Without tag review, other users can tag you in compromising locations, unwanted photos, or scam promotions automatically.",
        "remediation": "Enable 'Review posts you are tagged in before they appear on your timeline' across all platforms.",
        "severity": "HIGH",
        "finding_title": "Tag review approval queue disabled"
    },
    {
        "id": "q_tag_2",
        "category_id": "tagging_mentions",
        "question": "Can anyone tag you in photos or posts without your explicit permission?",
        "options": ["YES", "FRIENDS_ONLY", "NO"],
        "risk_mapping": {"YES": 90, "FRIENDS_ONLY": 35, "NO": 0},
        "explanation": "Open tagging permissions expose you to mass spam campaigns and malicious cryptocurrency scam tagging rings.",
        "remediation": "Restrict tagging permissions strictly to approved friends or disable public tagging.",
        "severity": "HIGH",
        "finding_title": "Unrestricted tagging allowed by third parties"
    },
    {
        "id": "q_tag_3",
        "category_id": "tagging_mentions",
        "question": "Can strangers mention your handle (@username) in public comments or stories?",
        "options": ["YES", "FRIENDS_ONLY", "NO"],
        "risk_mapping": {"YES": 75, "FRIENDS_ONLY": 20, "NO": 0},
        "explanation": "Unfiltered mention access facilitates harassment, targeted phishing pings, and unwanted promotional notifications.",
        "remediation": "Restrict mention permissions to followers or mutual contacts.",
        "severity": "MEDIUM",
        "finding_title": "Unrestricted public mentions permitted"
    },
    {
        "id": "q_tag_4",
        "category_id": "tagging_mentions",
        "question": "Do you remove your tag or request deletion when someone posts an unflattering or location-revealing photo of you?",
        "options": ["YES", "SOMETIMES", "NO"],
        "risk_mapping": {"NO": 70, "SOMETIMES": 35, "YES": 0},
        "explanation": "Failing to remove unwanted tags permits external parties to leak your whereabouts even if your own feed is quiet.",
        "remediation": "Actively remove your tag from location-sensitive or unvetted photos posted by peers.",
        "severity": "LOW",
        "finding_title": "Passive tolerance of unwanted external tagging"
    },

    # ==========================================
    # CATEGORY G: Authentication & Security (Questions 27-31)
    # ==========================================
    {
        "id": "q_sec_1",
        "category_id": "account_security",
        "question": "Do you have Multi-Factor Authentication (MFA / 2FA) enabled on your social media accounts?",
        "options": ["YES", "NO", "NOT_SURE"],
        "risk_mapping": {"NO": 100, "NOT_SURE": 70, "YES": 0},
        "explanation": "Accounts without MFA are vulnerable to single-factor compromise via credential stuffing and data breach passwords.",
        "remediation": "Immediately enable MFA using an authenticator app (e.g. Google Authenticator, Aegis) or a hardware security key.",
        "severity": "CRITICAL",
        "finding_title": "Multi-Factor Authentication (MFA) disabled"
    },
    {
        "id": "q_sec_2",
        "category_id": "account_security",
        "question": "Do you reuse the same password across your social media account and other websites?",
        "options": ["YES", "SOMETIMES", "NO"],
        "risk_mapping": {"YES": 100, "SOMETIMES": 60, "NO": 0},
        "explanation": "Password reuse exposes your social media account whenever another unrelated third-party database is breached.",
        "remediation": "Deploy a dedicated password manager (Bitwarden, 1Password) to generate and store unique credentials for every account.",
        "severity": "CRITICAL",
        "finding_title": "Password reuse across multiple services"
    },
    {
        "id": "q_sec_3",
        "category_id": "account_security",
        "question": "Are unrecognized login alerts (email/push notifications) turned on for new device logins?",
        "options": ["YES", "NO", "NOT_SURE"],
        "risk_mapping": {"NO": 85, "NOT_SURE": 50, "YES": 0},
        "explanation": "Without login alerts, unauthorized sessions and account takeover activity will go completely unnoticed.",
        "remediation": "Turn on login alerts for unrecognized devices under security settings.",
        "severity": "HIGH",
        "finding_title": "Unrecognized login alerts disabled"
    },
    {
        "id": "q_sec_4",
        "category_id": "account_security",
        "question": "Do you regularly review active logged-in sessions and terminate unused or old devices?",
        "options": ["YES", "SOMETIMES", "NO"],
        "risk_mapping": {"NO": 80, "SOMETIMES": 40, "YES": 0},
        "explanation": "Stale sessions on old laptops, lab computers, or phones remain active indefinitely, creating persistent backdoor access.",
        "remediation": "Review the 'Where you are logged in' section and log out of all non-current sessions.",
        "severity": "MEDIUM",
        "finding_title": "Stale active sessions unmonitored"
    },
    {
        "id": "q_sec_5",
        "category_id": "account_security",
        "question": "Are your account recovery email and phone number up to date and secured with MFA?",
        "options": ["YES", "NO", "NOT_SURE"],
        "risk_mapping": {"NO": 90, "NOT_SURE": 55, "YES": 0},
        "explanation": "Outdated recovery channels can be claimed by new telephone number owners or compromised to bypass account locks.",
        "remediation": "Verify and refresh recovery email and mobile numbers; ensure the recovery email account also uses MFA.",
        "severity": "HIGH",
        "finding_title": "Unsecured or unverified account recovery options"
    },

    # ==========================================
    # CATEGORY H: Third-Party Apps (Questions 32-35)
    # ==========================================
    {
        "id": "q_app_1",
        "category_id": "third_party_apps",
        "question": "Do you periodically review and revoke permissions for connected third-party apps and quizzes?",
        "options": ["YES", "SOMETIMES", "NO"],
        "risk_mapping": {"NO": 90, "SOMETIMES": 50, "YES": 0},
        "explanation": "Viral personality quizzes and games often request wide OAuth read/write tokens that persist indefinitely.",
        "remediation": "Inspect 'Apps and Websites' in account settings and revoke access to all non-essential integrations.",
        "severity": "HIGH",
        "finding_title": "Unaudited third-party OAuth app authorizations"
    },
    {
        "id": "q_app_2",
        "category_id": "third_party_apps",
        "question": "Do you routinely use 'Sign in with Social Media' on random unfamiliar websites?",
        "options": ["YES", "SOMETIMES", "NO"],
        "risk_mapping": {"YES": 85, "SOMETIMES": 45, "NO": 0},
        "explanation": "Overusing social logins consolidates third-party breach blast radius and links your browsing activities together.",
        "remediation": "Use standalone email/passphrase combinations managed by a password manager or masked email relays.",
        "severity": "MEDIUM",
        "finding_title": "Heavy reliance on single-sign-on social tokens for unvetted sites"
    },
    {
        "id": "q_app_3",
        "category_id": "third_party_apps",
        "question": "Have you granted third-party tools permission to read your private direct messages or contacts?",
        "options": ["YES", "NOT_SURE", "NO"],
        "risk_mapping": {"YES": 100, "NOT_SURE": 60, "NO": 0},
        "explanation": "Giving third-party analytics or scheduling bots DM permissions compromises end-to-end user privacy and confidants.",
        "remediation": "Audit app scopes; immediately revoke permissions allowing third parties to read messages or contact address books.",
        "severity": "CRITICAL",
        "finding_title": "Direct message or contact book access granted to third parties"
    },
    {
        "id": "q_app_4",
        "category_id": "third_party_apps",
        "question": "Do you check what data permissions an application requests before approving authorization?",
        "options": ["YES", "SOMETIMES", "NO"],
        "risk_mapping": {"NO": 80, "SOMETIMES": 40, "YES": 0},
        "explanation": "Blindly consenting to OAuth access grants often yields excessive access far beyond the application's core functionality.",
        "remediation": "Practice least privilege: decline apps requesting excessive scopes like friend list or offline access.",
        "severity": "MEDIUM",
        "finding_title": "Lack of OAuth permission scope verification"
    },

    # ==========================================
    # CATEGORY I: Messaging & Social Engineering (Questions 36-40)
    # ==========================================
    {
        "id": "q_se_1",
        "category_id": "social_engineering",
        "question": "Have you ever shared a verification code, OTP, or password with anyone asking over chat or phone?",
        "options": ["YES", "NO"],
        "risk_mapping": {"YES": 100, "NO": 0},
        "explanation": "Verification codes (OTPs) are single-use session tokens; sharing them provides instant account takeover to scammers.",
        "remediation": "Never disclose authentication codes to anyone, including purported platform support agents.",
        "severity": "CRITICAL",
        "finding_title": "Verification OTP sharing vulnerability"
    },
    {
        "id": "q_se_2",
        "category_id": "social_engineering",
        "question": "Do you open links or download files sent by unfamiliar profiles in direct messages?",
        "options": ["YES", "SOMETIMES", "NO"],
        "risk_mapping": {"YES": 95, "SOMETIMES": 50, "NO": 0},
        "explanation": "Direct messages are a high-conversion delivery vector for phishing landing pages, credential grabbers, and malware.",
        "remediation": "Do not open unsolicited direct message links; verify the sender through a separate out-of-band channel.",
        "severity": "HIGH",
        "finding_title": "Susceptibility to direct message phishing links"
    },
    {
        "id": "q_se_3",
        "category_id": "social_engineering",
        "question": "Do you participate in social media quizzes asking for your first pet, mother's maiden name, or first car?",
        "options": ["YES", "SOMETIMES", "NO"],
        "risk_mapping": {"YES": 90, "SOMETIMES": 45, "NO": 0},
        "explanation": "Viral nostalgia quizzes are classic OSINT harvesting traps designed to gather answers to standard security questions.",
        "remediation": "Avoid interactive viral quizzes probing biographical trivia; use randomized answers for actual security questions.",
        "severity": "HIGH",
        "finding_title": "Participation in security-question harvesting quizzes"
    },
    {
        "id": "q_se_4",
        "category_id": "social_engineering",
        "question": "Can any account send you direct message requests without your prior approval?",
        "options": ["YES", "FRIENDS_ONLY", "NO"],
        "risk_mapping": {"YES": 80, "FRIENDS_ONLY": 20, "NO": 0},
        "explanation": "Unrestricted direct messaging exposes users to social engineering, sextortion scams, and harassing solicitations.",
        "remediation": "Configure message controls to filter unsolicited requests into a hidden spam review folder.",
        "severity": "MEDIUM",
        "finding_title": "Unfiltered direct messaging channels open"
    },
    {
        "id": "q_se_5",
        "category_id": "social_engineering",
        "question": "Do you double-check unexpected urgent requests for money or gift cards coming from an existing friend's profile?",
        "options": ["YES", "SOMETIMES", "NO"],
        "risk_mapping": {"NO": 95, "SOMETIMES": 50, "YES": 0},
        "explanation": "Compromised friend profiles are routinely used to broadcast emergency wire transfer or gift card scams to contacts.",
        "remediation": "Always call your friend on a trusted phone number before sending money or gift cards.",
        "severity": "HIGH",
        "finding_title": "Vulnerability to urgent impersonation/emergency scams"
    },

    # ==========================================
    # CATEGORY J: Digital Footprint (Questions 41-45)
    # ==========================================
    {
        "id": "q_df_1",
        "category_id": "digital_footprint",
        "question": "Do you regularly audit and purge old historical posts from several years ago?",
        "options": ["YES", "SOMETIMES", "NO"],
        "risk_mapping": {"NO": 85, "SOMETIMES": 40, "YES": 0},
        "explanation": "Historical posts frequently contain outdated opinions, forgotten location breadcrumbs, and personal landmarks.",
        "remediation": "Use platform bulk-archive tools to archive or delete posts older than 12-24 months.",
        "severity": "MEDIUM",
        "finding_title": "Legacy historical posts uncurated"
    },
    {
        "id": "q_df_2",
        "category_id": "digital_footprint",
        "question": "Do you have unused or forgotten social media accounts that you haven't logged into for over a year?",
        "options": ["YES", "NOT_SURE", "NO"],
        "risk_mapping": {"YES": 85, "NOT_SURE": 50, "NO": 0},
        "explanation": "Zombie accounts that are neglected remain vulnerable to unnoticed takeovers and credential stuffing leaks.",
        "remediation": "Locate and formally delete or lock down dormant legacy profiles on Tumblr, Flickr, Ask.fm, X, etc.",
        "severity": "MEDIUM",
        "finding_title": "Dormant zombie accounts left unattended"
    },
    {
        "id": "q_df_3",
        "category_id": "digital_footprint",
        "question": "Have you searched your own name, phone number, and username on search engines to see what is publicly indexed?",
        "options": ["YES", "SOMETIMES", "NO"],
        "risk_mapping": {"NO": 75, "SOMETIMES": 35, "YES": 0},
        "explanation": "Self-doxxing audits (regularly searching for your own footprint) help identify unintended public data leaks early.",
        "remediation": "Conduct self-OSINT audits every 6 months and submit removal requests for data broker websites.",
        "severity": "LOW",
        "finding_title": "No regular self-OSINT exposure assessments performed"
    },
    {
        "id": "q_df_4",
        "category_id": "digital_footprint",
        "question": "Do you use the exact same username / handle across every single online platform?",
        "options": ["YES", "SOMETIMES", "NO"],
        "risk_mapping": {"YES": 80, "SOMETIMES": 40, "NO": 0},
        "explanation": "Identical handles across services allow cross-platform correlation tools (e.g. Sherlock, WhatsMyName) to stitch your full digital identity together.",
        "remediation": "Vary your handles between professional, personal, and anonymous gaming or developer accounts.",
        "severity": "MEDIUM",
        "finding_title": "Global username reuse across multiple platforms"
    },
    {
        "id": "q_df_5",
        "category_id": "digital_footprint",
        "question": "Do you maintain a bio link-tree aggregator containing links to all your personal documents, wishlists, and websites?",
        "options": ["YES", "SOMETIMES", "NO"],
        "risk_mapping": {"YES": 75, "SOMETIMES": 35, "NO": 0},
        "explanation": "Public link aggregators consolidate dispersed digital trails into a single targetable dossier for threat actors.",
        "remediation": "Prune link-in-bio aggregators to remove links disclosing sensitive registries, personal wishlists, or resumes with contact details.",
        "severity": "LOW",
        "finding_title": "Centralized link aggregator exposing consolidated footprints"
    }
]

def get_all_questions() -> list:
    return QUESTIONS

def get_question_by_id(qid: str) -> dict:
    for q in QUESTIONS:
        if q["id"] == qid:
            return q
    return None

def get_categories() -> dict:
    return CATEGORIES
