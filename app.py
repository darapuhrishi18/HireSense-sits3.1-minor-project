from flask import Flask, render_template, request, send_file
import os
from werkzeug.utils import secure_filename

from services.pdf_generator import generate_resume_pdf
from services.resume_parser import extract_resume_text
from services.scoring import calculate_skill_score, get_score_category
from services.grok_service import analyze_resume_with_grok
from agents.gap_agent import analyze_gaps
from agents.resource_agent import get_resources
from services.job_search import generate_job_links


app = Flask(__name__)


# =========================================================
# FOLDERS
# =========================================================

# Vercel filesystem is read-only except for /tmp.
# Locally, continue using normal project folders.

if os.environ.get("VERCEL") == "1":
    UPLOAD_FOLDER = "/tmp/uploads"
    GENERATED_FOLDER = "/tmp/generated_resumes"
else:
    UPLOAD_FOLDER = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "uploads"
    )

    GENERATED_FOLDER = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "generated_resumes"
    )


ALLOWED_EXTENSIONS = {"pdf", "docx"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["GENERATED_FOLDER"] = GENERATED_FOLDER

# Maximum upload size: 10 MB
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024


# =========================================================
# CREATE WRITABLE FOLDERS
# =========================================================

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["GENERATED_FOLDER"], exist_ok=True)


# =========================================================
# FILE VALIDATION
# =========================================================

def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# =========================================================
# WELCOME PAGE
# =========================================================

@app.route("/")
def home():
    return render_template("welcome.html")


# =========================================================
# RESUME ANALYZER PAGE
# =========================================================

@app.route("/analyzer")
def analyzer():
    return render_template("index.html")


# =========================================================
# ANALYZE RESUME
# =========================================================

@app.route("/analyze", methods=["POST"])
def analyze():

    # -----------------------------------------------------
    # Get uploaded resume
    # -----------------------------------------------------

    resume = request.files.get("resume")

    job_description = request.form.get(
        "job_description",
        ""
    ).strip()

    linkedin_url = request.form.get(
        "linkedin_url",
        ""
    ).strip()


    # -----------------------------------------------------
    # Check resume
    # -----------------------------------------------------

    if not resume or resume.filename == "":
        return "Please upload a PDF or DOCX resume.", 400

    if not allowed_file(resume.filename):
        return "Only PDF and DOCX resumes are supported.", 400


    # -----------------------------------------------------
    # Check job information
    # -----------------------------------------------------

    if not job_description and not linkedin_url:
        return "Please enter a job description or LinkedIn job URL.", 400


    # -----------------------------------------------------
    # Save uploaded resume
    # -----------------------------------------------------

    filename = secure_filename(resume.filename)

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    try:
        resume.save(filepath)

    except Exception as exc:
        return f"Could not save the uploaded resume: {exc}", 500


    # -----------------------------------------------------
    # Extract resume text
    # -----------------------------------------------------

    try:

        resume_text = extract_resume_text(filepath)

    except Exception as exc:

        return f"Could not read the resume: {exc}", 500


    # =====================================================
    # GROQ AI RESUME ANALYSIS
    # =====================================================

    try:

        ai_analysis = analyze_resume_with_grok(
            resume_text
        )

    except Exception as exc:

        print("Groq analysis error:", exc)

        ai_analysis = (
            "Groq AI analysis could not be completed. "
            f"Error: {exc}"
        )


    # -----------------------------------------------------
    # LinkedIn URL handling
    # -----------------------------------------------------

    if not job_description:

        job_description = (
            "LinkedIn job URL supplied. "
            "For this MVP, paste the job description "
            "as well so the matching engine can analyze it."
        )


    # =====================================================
    # CALCULATE RESUME MATCH SCORE
    # =====================================================

    try:

        result = calculate_skill_score(
            resume_text,
            job_description
        )

    except Exception as exc:

        print("Scoring error:", exc)

        return f"Resume scoring failed: {exc}", 500


    score = result["score"]

    category = get_score_category(score)


    # =====================================================
    # ANALYZE MISSING SKILLS
    # =====================================================

    try:

        gap_result = analyze_gaps(
            result["missing_skills"],
            score
        )

    except Exception as exc:

        print("Gap analysis error:", exc)

        gap_result = {
            "drawbacks": [],
            "recommendations": [],
            "estimated_improvement": 0
        }


    # =====================================================
    # GET LEARNING RESOURCES
    # =====================================================

    try:

        resources = get_resources(
            result["missing_skills"]
        )

    except Exception as exc:

        print("Resource agent error:", exc)

        resources = []


    # =====================================================
    # GENERATE JOB SEARCH LINKS
    # =====================================================

    try:

        job_links = generate_job_links(
            result["resume_skills"]
        )

    except Exception as exc:

        print("Job search error:", exc)

        job_links = []


    # =====================================================
    # PDF GENERATION
    #
    # PDF WILL ONLY BE GENERATED WHEN SCORE >= 85
    # =====================================================

    pdf_path = None
    pdf_filename = None

    if score >= 85:

        try:

            pdf_path = generate_resume_pdf(
                filename=filename,
                resume_text=resume_text,
                score=score,
                output_folder=app.config["GENERATED_FOLDER"]
            )

            if pdf_path:
                pdf_filename = os.path.basename(pdf_path)

        except Exception as exc:

            print("PDF generation error:", exc)

            pdf_path = None
            pdf_filename = None


    # =====================================================
    # SHOW RESULT PAGE
    # =====================================================

    return render_template(

        "result.html",

        # -------------------------------------------------
        # Resume information
        # -------------------------------------------------

        filename=filename,

        linkedin_url=linkedin_url,


        # -------------------------------------------------
        # GROQ AI ANALYSIS
        # -------------------------------------------------

        ai_analysis=ai_analysis,


        # -------------------------------------------------
        # Score information
        # -------------------------------------------------

        score=score,

        category=category,


        # -------------------------------------------------
        # Skills
        # -------------------------------------------------

        matched_skills=result["matched_skills"],

        missing_skills=result["missing_skills"],

        resume_skills=result["resume_skills"],

        required_skills=result["required_skills"],


        # -------------------------------------------------
        # AI improvement analysis
        # -------------------------------------------------

        drawbacks=gap_result["drawbacks"],

        recommendations=gap_result["recommendations"],

        estimated_improvement=gap_result[
            "estimated_improvement"
        ],


        # -------------------------------------------------
        # Learning resources
        # -------------------------------------------------

        resources=resources,


        # -------------------------------------------------
        # Job recommendations
        # -------------------------------------------------

        job_links=job_links,


        # -------------------------------------------------
        # PDF information
        # -------------------------------------------------

        pdf_path=pdf_path,

        pdf_filename=pdf_filename
    )


# =========================================================
# DOWNLOAD GENERATED PDF
# =========================================================

@app.route("/download-pdf/<filename>")
def download_pdf(filename):

    # Prevent unsafe path traversal
    filename = secure_filename(filename)

    pdf_path = os.path.join(
        app.config["GENERATED_FOLDER"],
        filename
    )


    # Check whether PDF exists
    if not os.path.exists(pdf_path):

        return "PDF not found.", 404


    # Send PDF to browser
    return send_file(
        pdf_path,
        as_attachment=True,
        download_name=filename,
        mimetype="application/pdf"
    )


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/health")
def health():

    return {
        "status": "ok",
        "message": "AI Resume Agent is running"
    }


# =========================================================
# RUN APPLICATION LOCALLY
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )