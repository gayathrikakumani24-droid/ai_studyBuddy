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


def generate_quiz(topic):
    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=f"""
      Create exactly 5 multiple-choice questions on the topic below.

    STRICT RULES (DO NOT VIOLATE):
    - Use Markdown formatting
    - Each question must be numbered (Q1, Q2, ...)
    - Each option MUST be on a separate line
    - Each option must start with A., B., C., D.
    - Do NOT combine options into a sentence or paragraph
    - Leave a blank line between questions

    FORMAT (FOLLOW EXACTLY):

    Q1. Question text  
    A. Option one  
    B. Option two  
    C. Option three  
    D. Option four  

    Answer: B

    Topic:{topic}"""
    )
    return response.text
