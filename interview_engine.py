import random
from interview_questions import INTERVIEW_QUESTIONS

def get_questions(role, level, asked_questions):

    all_questions = INTERVIEW_QUESTIONS[role][level]

    remaining = [q for q in all_questions if q not in asked_questions]

    if len(remaining) < 5:
        remaining = all_questions

    return random.sample(remaining,5)

def evaluate_answer(answer, keywords):

    score = 0

    for word in keywords:
        if word.lower() in answer.lower():
            score += 1

    return score