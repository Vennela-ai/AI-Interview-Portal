import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_questions(role, experience, skills):

    prompt = f"""
You are an expert technical interviewer.

Generate exactly 10 interview questions.

Job Role: {role}
Experience: {experience}
Skills: {skills}

Rules:
- 3 HR questions
- 5 Technical questions
- 2 Scenario-based questions

Return only the numbered questions.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text
def evaluate_answers(questions, answers):
    prompt = f"""
You are an experienced technical interviewer.

Evaluate the candidate's answers.

Return the response in exactly this format:

Overall Score: XX/100

Technical Skills:
- ...

Communication:
- ...

Strengths:
- Point 1
- Point 2
- Point 3

Weaknesses:
- Point 1
- Point 2

Suggestions:
- Point 1
- Point 2
- Point 3

Candidate Answers:
{answers}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text