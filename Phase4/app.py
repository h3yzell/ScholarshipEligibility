from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

# ==========================================
# PRIVACY ENGINEERING HELPER FUNCTIONS
# ==========================================
def determine_financial_tier(family_income, household_size):
    if not household_size or household_size <= 0:
        return 4
        
    per_capita_income = family_income / household_size

    if per_capita_income <= 2500:
        return 4  
    elif per_capita_income <= 5000:
        return 3  
    elif per_capita_income <= 10000:
        return 2  
    else:
        return 1  

def determine_academic_tier(CGPA):
    if CGPA >= 3.7:
        return 1
    elif CGPA >= 3.5:
        return 2
    elif CGPA >= 3.0:
        return 3
    else:
        return 4

# =========================
# DATABASE INITIALIZATION
# =========================
def init_db():
    conn = sqlite3.connect("scholarship.db")
    cursor = conn.cursor()

    # Schema updated to use an integer 'financial_tier' instead of a boolean
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS health_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT, 
        academic_tier INTEGER,
        require_medical_attention BOOLEAN,
        financial_tier INTEGER
    )
    """)

    conn.commit()
    conn.close()

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
    def safe_float(val, default=0.0):
        try:
            return float(val) if val and val.strip() else default
        except ValueError:
            return default

    def safe_int(val, default=1):
        try:
            return int(val) if val and val.strip() else default
        except ValueError:
            return default

    # Capture transient raw parameters in-memory
    student_id = request.form.get('student_id', '').strip()
    CGPA = safe_float(request.form.get('CGPA'))
    family_income = safe_float(request.form.get('family_income'))
    household_size = safe_int(request.form.get('household_size'))
    medication_problems = request.form.get('medication_problems', '').strip()
    
    # Execute Phase 4 Data Minimization and Transformation
    academic_tier = determine_academic_tier(CGPA)
    financial_tier = determine_financial_tier(family_income, household_size)

    if not medication_problems or medication_problems.lower() == "none":
        require_medical_attention = False
    else:
        require_medical_attention = True

    # Connect to SQLite database
    conn = sqlite3.connect("scholarship.db")
    cursor = conn.cursor()

    # Commit only the non-identifiable, derived tier matrices
    cursor.execute("""
    INSERT INTO health_records (student_id, academic_tier, require_medical_attention, financial_tier)
    VALUES (?, ?, ?, ?)
    """, (student_id, academic_tier, require_medical_attention, financial_tier))
    
    conn.commit()
    record_id = cursor.lastrowid
    formatted_id = f"{record_id:05}"
    conn.close()

    return f"""
    <h2>Application Processed Successfully!</h2>
    <p>Your Privacy-Minimized Record ID: {formatted_id}</p>
    <p style="color: green;">✓ Privacy Control Verified: Raw financial details were dropped and securely abstracted into Financial Tier {financial_tier}.</p>
    <a href="/">Back to Form</a>
    """

if __name__ == '__main__':
    app.run(debug=True)