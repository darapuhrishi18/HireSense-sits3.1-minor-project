from urllib.parse import quote_plus


def youtube_link(skill):
    query = quote_plus(f"{skill} tutorial")
    return f"https://www.youtube.com/results?search_query={query}"


def coursera_link(skill):
    query = quote_plus(skill)
    return f"https://www.coursera.org/search?query={query}"


def udemy_link(skill):
    query = quote_plus(skill)
    return f"https://www.udemy.com/courses/search/?q={query}"


def google_link(skill):
    query = quote_plus(f"{skill} course tutorial")
    return f"https://www.google.com/search?q={query}"


def get_resources(missing_skills):

    resources = []
    used_skills = set()

    if not missing_skills:
        return resources

    for skill in missing_skills:

        skill = str(skill).strip()

        if not skill:
            continue

        skill_key = skill.lower()

        # Don't show duplicate skills
        if skill_key in used_skills:
            continue

        used_skills.add(skill_key)

        # ------------------------------------------------
        # ONLY RESOURCES RELATED TO THIS MISSING SKILL
        # ------------------------------------------------

        resources.append({
            "skill": skill,
            "title": f"{skill} - YouTube Tutorials",
            "description": f"Learn {skill} through practical video tutorials.",
            "url": youtube_link(skill)
        })

        resources.append({
            "skill": skill,
            "title": f"{skill} - Coursera Courses",
            "description": f"Find structured courses related to {skill}.",
            "url": coursera_link(skill)
        })

        resources.append({
            "skill": skill,
            "title": f"{skill} - Udemy Courses",
            "description": f"Find practical training and courses for {skill}.",
            "url": udemy_link(skill)
        })

        resources.append({
            "skill": skill,
            "title": f"{skill} - More Learning Resources",
            "description": f"Find tutorials, documentation and learning material for {skill}.",
            "url": google_link(skill)
        })

    return resources