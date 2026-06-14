import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Create Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def explain_topic(topic):
    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=f"Explain the following topic in simple terms:\n{topic}"
    )
    return response.text


def summarize_notes(notes):
    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=f"Summarize the following notes into bullet points:\n{notes}"
    )
    return response.text


def generate_study_plan(subjects, difficulty, days):
    prompt = f"""
    Create a clear and practical study plan based on the following details.

    Subjects:
    {subjects}

    Difficulty level of subjects:
    {difficulty}

    Total available study days:
    {days}

    RULES:
    - Generate a day-wise study plan
    - Allocate more time to difficult subjects
    - Include revision days
    - Keep daily tasks short and realistic
    - Use bullet points
    - Do NOT write paragraphs
    - Keep the format clean and readable

    FORMAT (FOLLOW EXACTLY):

    Day 1:
    - Subject: <name>
    - Topics to study: <topics>

    Day 2:
    - Subject: <name>
    - Topics to study: <topics>

    End with a short revision strategy.
    """
    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )
    return response.text


def generate_quiz(topic, q_count=5, q_type="MCQ", q_diff="Medium", include_answers=True):
    """
    Generate a quiz as a JSON array of question objects.

    Each object has:
      - question: str
      - type: "mcq" | "truefalse" | "shortanswer"
      - options: list[str]  (empty for short answer)
      - answer: str         (the correct option text or True/False)
      - explanation: str
    """
    prompt = f"""You are a quiz generator. Generate exactly {q_count} quiz questions on the topic below.
Question type: {q_type}
Difficulty: {q_diff}
Topic / Content:
{topic}

Return a JSON array. Each element must follow one of these schemas:

MCQ example:
{{"question": "What is X?", "type": "mcq", "options": ["A", "B", "C", "D"], "answer": "A", "explanation": "Because..."}}

True/False example:
{{"question": "X is true.", "type": "truefalse", "options": ["True", "False"], "answer": "True", "explanation": "Because..."}}

Short Answer example:
{{"question": "What is X?", "type": "shortanswer", "options": [], "answer": "Expected answer", "explanation": "Because..."}}

Rules:
- For MCQ, always provide exactly 4 options. "answer" must exactly match one option string.
- For Mixed type, use a variety of the above types.
- Output ONLY the raw JSON array, nothing else.
"""
    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt,
        config={"response_mime_type": "application/json"},
    )
    return response.text