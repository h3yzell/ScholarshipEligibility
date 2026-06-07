from flask import Flask, request, render_template
from pymongo import MongoClient
import datetime

app = Flask(__name__)

# ==========================================
# MONGO DATABASE INITIALIZATION
# ==========================================
# Connect to local MongoDB instance
client = MongoClient("mongodb://localhost:27017/")
db = client["scholarship_system"]
collection = db["health_records"]

def init_db():
    print("Initializing MongoDB collections and TTL indexes...")
    # Create a native TTL index on the "expires_at" field.
    # expireAfterSeconds=0 tells Mongo to delete the document exactly when the clock hits 'expires_at'
    collection.create_index("expires_at", expireAfterSeconds=0)

init_db()

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

    # Capture raw form entries
    student_id = request.form.get('student_id', '').strip()
    CGPA = safe_float(request.form.get('CGPA'))
    family_income = safe_float(request.form.get('family_income'))
    household_size = safe_int(request.form.get('household_size'))
    medication_problems = request.form.get('medication_problems', '').strip()
    
    # Process privacy abstractions
    academic_tier = determine_academic_tier(CGPA)
    financial_tier = determine_financial_tier(family_income, household_size)
    require_medical_attention = False if (not medication_problems or medication_problems.lower() == "none") else True

    # MongoDB CRITICAL: Native TTL indexes require a standard Python datetime object, NOT an ISO string
    retention_days = 30
    expiration_datetime = datetime.datetime.utcnow() + datetime.timedelta(days=retention_days)

    # Build document dictionary payload
    application_document = {
        "student_id": student_id,
        "academic_tier": academic_tier,
        "require_medical_attention": require_medical_attention,
        "financial_tier": financial_tier,
        "expires_at": expiration_datetime  # Tracked by native TTL background loop
    }

    # Insert into MongoDB collection
    result = collection.insert_one(application_document)
    
    # Convert MongoDB's native ObjectId to a readable string representation
    formatted_id = str(result.inserted_id)

    return f"""
    <h2>Application Logged inside MongoDB!</h2>
    <p>Your Document Object ID: {formatted_id}</p>
    <p style="color: blue;">⏱️ Native MongoDB TTL Active: Document will be dropped automatically by MongoDB's background thread in 30 days.</p>
    <a href="/">Back to Form</a>
    """

if __name__ == '__main__':
    app.run(debug=True)