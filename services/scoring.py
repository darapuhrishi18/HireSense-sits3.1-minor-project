import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing from .env")

client = Groq(api_key=api_key)


# =========================================================
# GROQ-BASED RESUME / JOB MATCHING
# =========================================================

def calculate_skill_score(resume_text, job_text):

    prompt = f"""
You are an expert recruitment and resume-matching AI.

Compare the candidate's resume with the job description.

IMPORTANT:
The resume can belong to ANY profession or industry.

Examples:
- Teaching
- Nursing
- Accounting
- Finance
- HR
- Marketing
- AI/ML
- Software Engineering
- Civil Engineering
- Mechanical Engineering
- Electrical Engineering
- Healthcare
- Sales
- Administration
- Legal
- Hospitality
- Any other profession

Do NOT assume that the candidate is an AI/ML or software candidate.

Analyze the actual content of the resume and job description.

Evaluate:

1. Technical/professional skills
2. Soft skills
3. Education requirements
4. Experience requirements
5. Certifications
6. Job responsibilities
7. Domain knowledge
8. Tools/technologies
9. Overall suitability

Calculate a realistic match score from 0 to 100.

Use this interpretation:

0-49   = Major improvement required
50-59  = More improvement required
60-74  = Possibility of improvement
75-84  = Good / Better match
85-100 = Excellent match

Return ONLY valid JSON using exactly this structure:

{{
    "score": 0,
    "candidate_profession": "",
    "matched_skills": [],
    "missing_skills": [],
    "required_skills": [],
    "resume_skills": [],
    "strengths": [],
    "drawbacks": [],
    "recommendations": []
}}

RESUME:
-------------------------
{resume_text}
-------------------------

JOB DESCRIPTION:
-------------------------
{job_text}
-------------------------

Return ONLY JSON.
"""

    try:

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional recruitment AI. "
                        "Match resumes and jobs from any profession. "
                        "Return only valid JSON."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1
        )

        content = response.choices[0].message.content.strip()

        # Remove markdown code fences if the model adds them
        if content.startswith("```"):
            content = content.replace("```json", "")
            content = content.replace("```", "")
            content = content.strip()

        result = json.loads(content)

        # Make sure score is a valid number
        score = int(result.get("score", 0))
        score = max(0, min(100, score))

        return {
            "score": score,
            "resume_skills": result.get("resume_skills", []),
            "required_skills": result.get("required_skills", []),
            "matched_skills": result.get("matched_skills", []),
            "missing_skills": result.get("missing_skills", []),
            "candidate_profession": result.get(
                "candidate_profession", ""
            ),
            "strengths": result.get("strengths", []),
            "drawbacks": result.get("drawbacks", []),
            "recommendations": result.get("recommendations", [])
        }

    except Exception as exc:

        print("Groq scoring error:", exc)

        return {
            "score": 0,
            "resume_skills": [],
            "required_skills": [],
            "matched_skills": [],
            "missing_skills": [],
            "candidate_profession": "",
            "strengths": [],
            "drawbacks": [
                "Unable to calculate the AI match score."
            ],
            "recommendations": [
                "Please try the analysis again."
            ]
        }


# =========================================================
# SCORE CATEGORY
# =========================================================

def get_score_category(score):

    if score < 50:
        return {
            "label": "Low Match",
            "message": "Major improvement is required."
        }

    if score < 60:
        return {
            "label": "Needs Improvement",
            "message": "More improvement is recommended."
        }

    if score < 75:
        return {
            "label": "Good Possibility",
            "message": "Your match can reasonably be improved."
        }

    if score < 85:
        return {
            "label": "Better",
            "message": "Your resume is a good match for this job."
        }

    return {
        "label": "Excellent",
        "message": "Your resume is highly compatible with this job."
    }