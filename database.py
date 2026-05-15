import pyodbc

connection = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=ResumeAnalyzerDB;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

cursor = connection.cursor()


def save_analysis(filename, ats_score, matched_skills, missing_skills):

    matched = ", ".join(matched_skills)

    missing = ", ".join(missing_skills)

    query = """
    INSERT INTO ResumeData
    (filename, ats_score, matched_skills, missing_skills)

    VALUES (?, ?, ?, ?)
    """

    cursor.execute(
        query,
        filename,
        ats_score,
        matched,
        missing
    )

    connection.commit()


def get_all_results():

    query = """
    SELECT * FROM ResumeData
    ORDER BY upload_date DESC
    """

    cursor.execute(query)

    return cursor.fetchall()