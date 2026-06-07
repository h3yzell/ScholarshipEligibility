from pymongo import MongoClient
import random
import datetime

# Setup Mongo Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["scholarship_system"]
collection = db["health_records"]

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

def seed_mongodb(records_count=10000):
    print("Clearing old collections and preparing fresh collection schema...")
    collection.drop()
    collection.create_index("expires_at", expireAfterSeconds=0)

    print(f"Generating {records_count} document structures in memory...")
    document_batch = []

    for i in range(1, records_count + 1):
        student_id = f"S{10000000 + i}"
        raw_cgpa = round(random.uniform(2.0, 4.0), 2)
        raw_income = round(random.uniform(1500.0, 45000.0), 2)
        raw_household = random.randint(1, 8)
        has_medical = random.random() < 0.20 

        # Transform raw attributes into anonymous tiers
        academic_tier = determine_academic_tier(raw_cgpa)
        financial_tier = determine_financial_tier(raw_income, raw_household)
        require_medical_attention = True if has_medical else False
        
        # Set a short 60-second expiration offset to make testing easier
        expiration_datetime = datetime.datetime.utcnow() + datetime.timedelta(days=30)

        # Assemble individual BSON-mappable document items
        doc = {
            "student_id": student_id,
            "academic_tier": academic_tier,
            "require_medical_attention": require_medical_attention,
            "financial_tier": financial_tier,
            "expires_at": expiration_datetime
        }
        document_batch.append(doc)

    print("Executing bulk Mongo transaction write...")
    result = collection.insert_many(document_batch)
    print(f"Successfully injected {len(result.inserted_ids)} records directly to MongoDB instance database.")

if __name__ == "__main__":
    seed_mongodb(10000)