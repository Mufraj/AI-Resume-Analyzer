import spacy

nlp = spacy.load("en_core_web_sm")

skills_list = [

    # Programming Languages
    "python",
    "java",
    "c++",
    "c",
    "c#",
    "javascript",
    "typescript",
    "php",
    "ruby",
    "swift",
    "kotlin",

    # Web Development
    "html",
    "css",
    "react",
    "angular",
    "vue",
    "node.js",
    "express",
    "flask",
    "django",
    "bootstrap",

    # Databases
    "sql",
    "mysql",
    "mongodb",
    "postgresql",
    "firebase",

    # AI / Data Science
    "machine learning",
    "deep learning",
    "data science",
    "artificial intelligence",
    "nlp",
    "computer vision",
    "tensorflow",
    "pytorch",
    "pandas",
    "numpy",

    # Cloud / DevOps
    "aws",
    "azure",
    "docker",
    "kubernetes",
    "git",
    "github",

    # Soft Skills
    "communication",
    "teamwork",
    "leadership",
    "problem solving",
    "time management"
]


def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in skills_list:

        if skill in text:
            found_skills.append(skill)

    return found_skills