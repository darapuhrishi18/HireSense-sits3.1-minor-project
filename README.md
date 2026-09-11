# AI Resume & Job Application Agent

Beginner-friendly Flask MVP for resume/job matching.

## Run in VS Code

1. Open this folder in VS Code.
2. Open Terminal.
3. Create environment:
   `python -m venv venv`
4. Activate:
   PowerShell:
   `.\venv\Scripts\Activate.ps1`
5. If PowerShell blocks activation:
   `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`
   then run activation again.
6. Install:
   `pip install -r requirements.txt`
7. Start:
   `python app.py`
8. Open:
   `http://127.0.0.1:5000`

## Current MVP

- PDF/DOCX resume upload
- Resume text extraction
- Job description input
- Skill matching
- Match score
- Missing skills
- Drawbacks
- Improvement suggestions
- Learning resources
- Basic health endpoint

## Next phases

- Supabase database and storage
- LLM/AI agents
- Semantic matching
- Resume optimizer
- ATS validation
- Automatic improved PDF generation
- Permitted/public job-source integration
- Job recommendation dashboard

Never commit `.env` or secret API keys to GitHub.
