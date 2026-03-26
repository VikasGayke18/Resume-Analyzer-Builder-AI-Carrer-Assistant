from interview_questions import INTERVIEW_QUESTIONS

EXPECTED_ANSWERS = {}

for role in INTERVIEW_QUESTIONS:
    for level in INTERVIEW_QUESTIONS[role]:
        for item in INTERVIEW_QUESTIONS[role][level]:
            if isinstance(item, dict):
                EXPECTED_ANSWERS[item["q"]] = item["answer"]