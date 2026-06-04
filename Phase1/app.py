from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

# =========================
# DATABASE INITIALIZATION
# =========================
def init_db():

    conn = sqlite3.connect("scholarship.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS health_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        student_id TEXT,
        ic TEXT,
        education TEXT,
        phone TEXT,
        CGPA FLOAT,
        medication_problems TEXT,
        family_income FLOAT,
        household_size INTEGER
    )
    """)

    conn.commit()
    conn.close()

# Run database setup
init_db()

# =========================
# HOME PAGE
# =========================
@app.route('/')
def home():
    return render_template('index.html')

# =========================
# FORM SUBMISSION
# =========================
@app.route('/submitForm', methods=['POST'])
def submit_form():

    # Get data from HTML form
    name = request.form.get('name')
    student_id = request.form.get('student_id')
    ic = request.form.get('ic')
    education = request.form.get('education')
    phone = request.form.get('phone')
    CGPA = float(request.form.get('CGPA'))
    medication_problems = request.form.get('medication_problems')
    family_income = float(request.form.get('family_income'))
    household_size = int(request.form.get('household_size'))

    # Connect to SQLite database
    conn = sqlite3.connect("scholarship.db")
    cursor = conn.cursor()

    # Insert data into table
    cursor.execute("""
    INSERT INTO health_records
    (name, student_id, ic, education, phone, CGPA, medication_problems, family_income, household_size)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, student_id, ic, education, phone, CGPA, medication_problems, family_income, household_size))

    conn.commit()
    record_id = cursor.lastrowid
    formatted_id = f"{record_id:05}"
    conn.close()

    return f"""
    <h2>Health Data Submitted Successfully!</h2>

    <p>Your Record ID: {formatted_id}</p>

    <a href="/">Back to Form</a>
    """
if __name__ == '__main__':
    app.run(debug=True)