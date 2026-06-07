import sqlite3
import random

DB_NAME = "scholarship.db"

# ==========================================
# PRIVACY ENGINEERING HELPER FUNCTIONS 
# (Mirrored from app.py to ensure identical mapping)
# ==========================================
def determine_financial_tier(family_income, household_size):
    if not household_size or household_size <= 0:
        return 4
        
    per_capita_income = family_income / household_size

    if per_capita_income <= 2500:
        return 4  # Low income / High assistance tier
    elif per_capita_income <= 5000:
        return 3  
    elif per_capita_income <= 10000:
        return 2  
    else:
        return 1  # High income / Low assistance tier

def determine_academic_tier(CGPA):
    if CGPA >= 3.7:
        return 1
    elif CGPA >= 3.5:
        return 2
    elif CGPA >= 3.0:
        return 3
    else:
        return 4

# ==========================================
# SEED SCRIPT EXECUTION
# ==========================================
def seed_database(records_count=10000):
    print(f"Connecting to {DB_NAME}...")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Ensure the table is created before trying to seed it
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS health_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT, 
        academic_tier INTEGER,
        require_medical_attention BOOLEAN,
        financial_tier INTEGER
    )
    """)

    print(f"Generating {records_count} privacy-minimized mock student profiles...")
    
    # Using a list to gather data for a fast batch insert
    data_batch = []
    
    for i in range(1, records_count + 1):
        # 1. Simulate Transient Inputs (In-memory only)
        student_num = 10000000 + i  
        student_id = f"S{student_num}"
        
        raw_cgpa = round(random.uniform(2.0, 4.0), 2)
        raw_income = round(random.uniform(1500.0, 45000.0), 2)
        raw_household = random.randint(1, 8)
        
        has_medical = random.random() < 0.20 
        
        # 2. Execute Privacy Attribute Transformations
        academic_tier = determine_academic_tier(raw_cgpa)
        financial_tier = determine_financial_tier(raw_income, raw_household)
        require_medical_attention = 1 if has_medical else 0

        # Append the tuple to our batch list instead of running individual SQL writes
        data_batch.append((student_id, academic_tier, require_medical_attention, financial_tier))

    # 3. Fast Batch Commit
    cursor.executemany("""
    INSERT INTO health_records (student_id, academic_tier, require_medical_attention, financial_tier)
    VALUES (?, ?, ?, ?)
    """, data_batch)
        
    conn.commit()
    conn.close()
    print(f"Successfully seeded {len(data_batch)} records into the database.")

if __name__ == "__main__":
    seed_database(10000)