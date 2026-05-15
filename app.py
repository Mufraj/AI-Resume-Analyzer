from flask import Flask, render_template, request
from analyzer import extract_skills
from database import save_analysis, get_all_results
import os
import pdfplumber

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def home():

    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():

    # Check Resume Upload
    if 'resume' not in request.files:
        return "No file uploaded"

    file = request.files['resume']

    if file.filename == '':
        return "No selected file"

    # Save Resume
    filepath = os.path.join(
        app.config['UPLOAD_FOLDER'],
        file.filename
    )

    file.save(filepath)

    # Extract Resume Text
    text = ""

    with pdfplumber.open(filepath) as pdf:

        for page in pdf.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted

    # Resume Skills
    skills = extract_skills(text)

    # Required Skills Input
    skills_input = request.form['skills_input']

    # Job Description
    job_description = request.form['job_description']

    # Combine Both Inputs
    combined_text = (
        skills_input + " " + job_description
    )

    # Extract Job Skills
    job_skills = extract_skills(combined_text)

    matched_skills = []
    missing_skills = []
    suggestions = []

    # Compare Skills
    for skill in job_skills:

        if skill in skills:
            matched_skills.append(skill)

        else:
            missing_skills.append(skill)

    # ATS Score
    if len(job_skills) > 0:

        ats_score = int(
            (len(matched_skills) / len(job_skills)) * 100
        )

    else:
        ats_score = 0

    # ATS Rating
    if ats_score >= 80:

        rating = "Excellent"

    elif ats_score >= 60:

        rating = "Good"

    else:

        rating = "Needs Improvement"

    # AI Suggestions
    if ats_score == 100:

        suggestions.append(
            "Excellent resume match for this job description."
        )

        suggestions.append(
            "Your resume is highly ATS optimized."
        )

        suggestions.append(
            "Consider adding more projects and certifications for stronger impact."
        )

    elif ats_score >= 60:

        suggestions.append(
            "Your resume matches many required skills."
        )

        suggestions.append(
            "Adding missing skills can further improve your ATS score."
        )

        for skill in missing_skills:

            suggestions.append(
                f"Consider learning {skill}."
            )

    else:

        suggestions.append(
            "Your resume needs improvement for this role."
        )

        suggestions.append(
            "Focus on adding the missing skills below."
        )

        for skill in missing_skills:

            suggestions.append(
                f"Learn {skill} to improve job matching."
            )

    # Save Analysis
    save_analysis(
        file.filename,
        ats_score,
        matched_skills,
        missing_skills
    )

    # Render Result Page
    return render_template(
        'result.html',
        ats_score=ats_score,
        rating=rating,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        suggestions=suggestions
    )


@app.route('/history')
def history():

    results = get_all_results()

    return render_template(
        'history.html',
        results=results
    )


if __name__ == '__main__':

    app.run(debug=True)