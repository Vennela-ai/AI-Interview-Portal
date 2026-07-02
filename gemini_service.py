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
You are an expert technical interviewer.

Evaluate the candidate's answers briefly and professionally.

Interview Questions:
{questions}

Candidate Answers:
{answers}

Rules:
- Keep the entire feedback under 200 words.
- Be direct and concise.
- Use short bullet points.
- Mention only the most important strengths and weaknesses.
- Focus on what the candidate should improve.

Return ONLY in this format:

## Overall Score
XX/100

## Technical Skills
Excellent / Good / Average / Needs Improvement

## Communication
Excellent / Good / Average / Needs Improvement

## Key Strengths
• Point 1
• Point 2

## Areas to Improve
• Point 1
• Point 2

## Focus Next
• Topic 1
• Topic 2
• Topic 3

## Final Verdict
One short sentence encouraging the candidate.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text