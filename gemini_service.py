import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_questions(
    role,
    experience,
    skills,
    difficulty,
    interview_type,
    question_count
):

    prompt = f"""
You are an expert interviewer.

Generate exactly {question_count} interview questions.

Job Role: {role}
Experience Level: {experience}
Primary Skill: {skills}
Difficulty Level: {difficulty}
Interview Type: {interview_type}

Instructions:

- Generate exactly {question_count} questions.
- Match the selected difficulty level.
- Focus on the selected primary skill.
- Keep all questions relevant to the selected job role.

If Interview Type is:
- Technical → Generate only technical questions.
- HR → Generate only HR questions.
- Behavioral → Generate only behavioral questions.
- Mixed → Generate a balanced mix of HR, technical, and scenario-based questions.

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

Interview Questions:
{questions}

Candidate Answers:
{answers}

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
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text