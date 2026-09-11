import os
from dotenv import load_dotenv
from groq import Groq

# Load variables from .env
load_dotenv()

# Get Groq API key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing from .env")

# Create Groq client
client = Groq(api_key=api_key)


def analyze_resume_with_grok(resume_text):

    prompt = f"""
You are an expert resume analyzer and career advisor.

Analyze this resume.

The resume can belong to ANY profession, including:
AI/ML, Software Engineering, Data Science,
Teaching, Nursing, Accounting, Finance,
HR, Marketing, Civil Engineering,
Mechanical Engineering, Electrical Engineering,
Healthcare, or any other profession.

Identify:

1. Candidate profession/domain
2. Education
3. Years of experience
4. Technical skills
5. Soft skills
6. Previous/current job roles
7. Suitable job roles
8. Suitable industries
9. Recommended skills to learn

Give a clear and useful analysis.

Resume:
--------------------
{resume_text}
--------------------

Give the answer in a clear, structured format.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "You are an expert resume analyzer and career advisor."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content