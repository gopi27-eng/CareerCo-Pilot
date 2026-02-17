"""
matcher.py — Keyword-based job matching for Gopi Borra
No API calls needed. Completely free. Runs forever without quota limits.

Scoring system:
  - Each matched keyword adds points
  - Job must hit a minimum score threshold to be considered a match
  - Instant disqualification for senior-only roles
"""

# ── Keywords that signal a GOOD match ──────────────────────────────────────

STRONG_KEYWORDS = [
    # Core skills
    "python", "sql", "machine learning", "data science", "deep learning",
    "nlp", "natural language", "neural network", "tensorflow", "pytorch",
    "scikit", "pandas", "numpy", "data analysis", "analytics",
    # Roles that fit
    "data scientist", "data analyst", "ml engineer", "ai engineer",
    "business analyst", "research analyst", "junior", "associate",
    "fresher", "entry level", "graduate", "intern", "trainee",
    # Tools Gopi knows
    "power bi", "tableau", "excel", "statistics", "regression",
    "classification", "clustering", "gen ai", "generative ai", "llm",
]

WEAK_KEYWORDS = [
    # Broader matches — worth fewer points
    "artificial intelligence", "big data", "cloud", "aws", "azure",
    "spark", "hadoop", "r programming", "visualization", "etl",
    "mysql", "postgresql", "mongodb", "api", "automation",
]

# ── Keywords that DISQUALIFY a job ─────────────────────────────────────────

DISQUALIFY_PHRASES = [
    "10+ years", "10 years", "12+ years", "15 years", "15+ years",
    "senior staff", "principal engineer", "director", "vp of",
    "vice president", "head of data", "chief", "cto", "cdo",
    "lead with 8", "lead with 7", "7+ years experience",
    "8+ years", "9+ years",
]

# ── Thresholds ──────────────────────────────────────────────────────────────

STRONG_WEIGHT = 2    # points per strong keyword hit
WEAK_WEIGHT   = 1    # points per weak keyword hit
MIN_SCORE     = 4    # minimum points to be considered a match


def is_good_match(job_description: str) -> bool:
    """
    Returns True if the job description is a good match for Gopi's profile.
    Pure keyword scoring — no API calls, no quota, no cost.
    """
    text = job_description.lower()

    # 1. Hard disqualification check
    for phrase in DISQUALIFY_PHRASES:
        if phrase in text:
            print(f"  ⛔ Disqualified — found: '{phrase}'")
            return False

    # 2. Score the job
    score = 0
    matched = []

    for kw in STRONG_KEYWORDS:
        if kw in text:
            score += STRONG_WEIGHT
            matched.append(kw)

    for kw in WEAK_KEYWORDS:
        if kw in text:
            score += WEAK_WEIGHT
            matched.append(kw)

    # 3. Decision
    if score >= MIN_SCORE:
        print(f"  ✅ Match (score={score}) — keywords: {', '.join(matched[:5])}")
        return True
    else:
        print(f"  ❌ No match (score={score}/{MIN_SCORE} needed)")
        return False