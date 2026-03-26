from pydoc import text

import pdfplumber
import re
import nltk
from nltk.corpus import stopwords
from ats_keywords import ROLE_KEYWORDS

nltk.download('stopwords')
STOPWORDS = set(stopwords.words('english'))

def extract_text(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def analyze_resume_text(text, role):

    import re

    text_original = text   # keep original for formatting check

    # 🔥 CLEAN TEXT
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)

    # =========================
    # 🔹 KEYWORDS
    # =========================
    ROLE_KEYWORDS = {
        "Software Developer": ["python","java","c++","javascript","react","node","git","docker","aws","api","sql"],
        "Data Analyst": ["python","sql","tableau","power bi","excel","statistics","pandas","numpy"],
        "AI Engineer": ["machine learning","deep learning","tensorflow","pytorch","nlp"],
        "Web Developer": ["html","css","javascript","react","node","mongodb"],
        "Cloud Engineer": ["aws","azure","gcp","docker","kubernetes"],
        "Cyber Security": ["network security","penetration testing","ethical hacking"],
        "DevOps Engineer": ["docker","kubernetes","jenkins","ci cd","terraform"]
    }

    keywords = ROLE_KEYWORDS.get(role, [])

    found_keywords = [k for k in keywords if k.lower() in text]
    missing_keywords = [k for k in keywords if k.lower() not in text]

    keyword_score = int((len(found_keywords)/len(keywords))*40) if keywords else 0

    # =========================
    # 🔹 SECTIONS (IMPROVED)
    # =========================
    section_patterns = {
        "Summary": ["summary", "profile"],
        "Skills": ["skills", "technical skills"],
        "Experience": ["experience", "work experience"],
        "Education": ["education"],
        "Projects": ["projects"]
    }

    found_sections = []

    for section, variants in section_patterns.items():
        if any(v in text for v in variants):
            found_sections.append(section)

    missing_sections = [s for s in section_patterns if s not in found_sections]

    section_score = int((len(found_sections)/len(section_patterns))*20)

    # =========================
    # 🔹 FORMATTING
    # =========================
    formatting_score = 0

    if "-" in text_original or "•" in text_original:
        formatting_score += 5

    if len(text_original) > 300:
        formatting_score += 5

    if "\n" in text_original:
        formatting_score += 5

    # =========================
    # 🔹 CONTACT
    # =========================
    contact_score = 0

    if re.search(r"\S+@\S+\.\S+", text_original):
        contact_score += 5

    if re.search(r"\d{10}", text_original):
        contact_score += 5

    # =========================
    # 🔹 ACTION WORDS
    # =========================
    action_words = [
        "develop", "build", "design", "implement",
        "create", "lead", "improve", "optimize"
    ]

    found_actions = []

    for word in action_words:
        if re.search(rf"\b{word}\w*\b", text):
            found_actions.append(word)

    action_score = int((len(found_actions)/len(action_words))*15)

    # =========================
    # 🎯 FINAL SCORE
    # =========================
    total_score = keyword_score + section_score + formatting_score + contact_score + action_score

    # =========================
    # 🔥 SUGGESTIONS (FIXED)
    # =========================
    suggestions = []

    if missing_keywords:
        suggestions.append("Add more relevant keywords for the selected role.")

    if missing_sections:
        suggestions.append("Add missing sections: " + ", ".join(missing_sections))

    if not found_actions:
        suggestions.append("Use strong action verbs like Developed, Built, Designed.")

    if formatting_score < 10:
        suggestions.append("Improve formatting (use bullet points, spacing).")

    if contact_score < 10:
        suggestions.append("Include proper email and phone number.")

# 🔥 FORCE AT LEAST 1 SUGGESTION
    if not suggestions:
        suggestions.append("Great resume! Just fine-tune formatting and add more impact.")

    print("DEBUG SUGGESTIONS:", suggestions)

    return {
        "role": role,
        "score": total_score,
        "found": found_keywords,
        "missing": missing_keywords,
        "sections_found": found_sections,
        "missing_sections": missing_sections,
        "action_words_used": found_actions,
        "suggestions": suggestions
    }