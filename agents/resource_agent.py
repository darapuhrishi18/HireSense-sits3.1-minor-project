RESOURCE_MAP = {
    "python": [
        ("Python Documentation", "https://docs.python.org/3/"),
        ("Build Python Projects", "https://www.python.org/about/gettingstarted/")
    ],
    "machine learning": [
        ("Scikit-learn Documentation", "https://scikit-learn.org/stable/")
    ],
    "tensorflow": [
        ("TensorFlow Tutorials", "https://www.tensorflow.org/tutorials")
    ],
    "docker": [
        ("Docker Get Started", "https://docs.docker.com/get-started/")
    ],
    "aws": [
        ("AWS Training", "https://aws.amazon.com/training/")
    ],
    "git": [
        ("Git Documentation", "https://git-scm.com/doc")
    ],
    "flask": [
        ("Flask Documentation", "https://flask.palletsprojects.com/")
    ],
    "rest api": [
        ("MDN HTTP Overview", "https://developer.mozilla.org/en-US/docs/Web/HTTP")
    ]
}


def get_resources(missing_skills):
    return {
        skill: RESOURCE_MAP.get(
            skill,
            [(f"Study {skill} fundamentals", "https://www.google.com/search?q=" + skill.replace(" ", "+") + "+tutorial")]
        )
        for skill in missing_skills
    }
