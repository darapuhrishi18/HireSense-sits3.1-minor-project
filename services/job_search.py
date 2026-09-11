from urllib.parse import quote


def generate_job_links(skills):
    jobs = []

    for skill in skills[:6]:
        encoded_skill = quote(skill)

        jobs.append({
            "title": f"{skill} Jobs",
            "skill": skill,
            "linkedin": f"https://www.linkedin.com/jobs/search/?keywords={encoded_skill}",
            "indeed": f"https://www.indeed.com/jobs?q={encoded_skill}"
        })

    return jobs