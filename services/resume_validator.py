def validate_resume(name="", email="", phone="", skills=None, education="", projects=""):
    skills = skills or []
    errors = []

    if not name:
        errors.append("Name is missing.")
    if not email:
        errors.append("Email is missing.")
    if not phone:
        errors.append("Phone number is missing.")
    if not skills:
        errors.append("Skills section is missing.")
    if not education:
        errors.append("Education section is missing.")
    if not projects:
        errors.append("Projects section is missing.")

    return {"passed": len(errors) == 0, "errors": errors}
