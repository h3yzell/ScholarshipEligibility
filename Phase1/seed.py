import sqlite3
import random

def seed_data():
    # Connect to your existing database
    conn = sqlite3.connect("scholarship.db")
    cursor = conn.cursor()

    # 20 Realistic Malaysian Dummy Data Profiles
    malaysian_dummy_data = [
        ("Muhammad Amirul bin Zainal", "S20145", "040314-14-5567", "Degree", "012-3456789", 3.85, "Asthma", 4500.00, 5),
        ("Nurul Aishah binti Mohd Rani", "S20146", "050822-10-6112", "Degree", "013-9876543", 3.42, "None", 3200.00, 6),
        ("Tan Wei Shen", "S20147", "041102-07-5433", "Diploma", "017-2233445", 3.91, "Eczema", 8500.00, 4),
        ("Priya a/p Subramaniam", "S20148", "030512-08-5994", "Degree", "011-1234567", 3.15, "None", 5500.00, 3),
        ("Ahmad Syamil bin Azman", "S20149", "040130-11-5021", "Foundation", "019-4455667", 2.80, "Migraine", 2500.00, 7),
        
        ("Chong Jia Ling", "S20150", "051215-14-5226", "Degree", "016-7788990", 3.67, "None", 12000.00, 4),
        ("Siti Khadijah binti Rahman", "S20151", "040404-03-5668", "Degree", "018-9900112", 3.50, "Allergic to Penicillin", 1800.00, 8),
        ("Divinesh a/l Naidu", "S20152", "031025-10-5115", "Diploma", "014-5566778", 3.28, "G6PD Deficiency", 6200.00, 5),
        ("Lim Kok Wai", "S20153", "040228-05-5087", "Degree", "012-8877665", 3.74, "None", 7000.00, 3),
        ("Farah Nabilah binti Rosli", "S20154", "050607-02-5334", "Foundation", "017-6655443", 3.05, "Anxiety", 4000.00, 5),
        
        ("Lee Ming Jie", "S20155", "040719-08-5913", "Degree", "013-4433221", 3.95, "None", 9500.00, 4),
        ("Arif Faisal bin Zulkapli", "S20156", "030911-14-5541", "Degree", "011-5566112", 2.92, "Sinusitis", 3100.00, 6),
        ("Kavitha a/p Balakrishnan", "S20157", "040505-10-5882", "Diploma", "019-2233889", 3.60, "None", 4800.00, 4),
        ("Khairul Anuar bin Ibrahim", "S20158", "021123-01-5223", "Degree", "016-3344556", 3.20, "High Blood Pressure", 5200.00, 5),
        ("Ng Mei Xin", "S20159", "050309-06-5114", "Degree", "012-9988776", 3.88, "Lactose Intolerance", 15000.00, 3),
        
        ("Amiruddin bin Hamzah", "S20160", "040812-14-6007", "Diploma", "014-2211334", 3.10, "Asthma", 2200.00, 7),
        ("Teoh Zhi Wei", "S20161", "041230-07-5555", "Degree", "017-8899112", 3.48, "None", 6800.00, 4),
        ("Thisha a/p Loganathan", "S20162", "050118-10-5336", "Foundation", "011-9988223", 3.71, "Dust Allergy", 3900.00, 5),
        ("Wan Nur Azlyn binti Wan Aziz", "S20163", "030202-03-5442", "Degree", "018-4455221", 3.55, "None", 5000.00, 6),
        ("Suresh a/l Ramasamy", "S20164", "040905-08-5671", "Degree", "013-7766554", 2.65, "None", 2900.00, 5)
    ]

    # Insert SQL Command
    cursor.executemany("""
    INSERT INTO health_records 
    (name, student_id, ic, education, phone, CGPA, medication_problems, family_income, household_size)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, malaysian_dummy_data)

    conn.commit()
    
    # Verify how many items are in the table now
    cursor.execute("SELECT COUNT(*) FROM health_records")
    total_records = cursor.fetchone()[0]
    
    conn.close()
    print(f"Successfully added 20 Malaysian dummy records!")
    print(f"Total rows currently in database: {total_records}")

if __name__ == "__main__":
    seed_data()