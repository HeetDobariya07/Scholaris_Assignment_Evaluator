import csv
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from flask import current_app

ASSIGNMENT_FIELDS = [
    'assignment_id', 'title', 'description',
    'subject', 'deadline', 'grading_criteria'
]

SUBMISSION_FIELDS = [
    'submission_id', 'assignment_id', 'student_id',
    'questions', 'evaluation'
]

def load_assignments(filename):
    assignments = {}
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                assignments[row['assignment_id']] = dict(row)
    return assignments

def save_assignment(filename, assignment_data):
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=ASSIGNMENT_FIELDS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(assignment_data)
    upload_assignments_to_mongodb()

def save_submission(filename, submission_data):
    """
    Append a new submission to the CSV file.
    - filename: path to the submissions CSV file
    - submission_data: dict with keys matching SUBMISSION_FIELDS
    """
    file_exists = os.path.isfile(filename)
    # Convert questions and evaluation to string for CSV storage
    data = submission_data.copy()
    if isinstance(data.get('questions'), list):
        data['questions'] = '|'.join(data['questions'])
    if isinstance(data.get('evaluation'), dict):
        data['evaluation'] = str(data['evaluation'])
    with open(filename, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=SUBMISSION_FIELDS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)
    upload_submissions_to_mongodb()

def update_submission(filename, submission_id, update_fields):
    """
    Update a submission in the CSV file by submission_id.
    - filename: path to the submissions CSV file
    - submission_id: the ID of the submission to update
    - update_fields: dict of fields to update (e.g., {'evaluation': {...}})
    """
    submissions = []
    updated = False
    # Read all submissions
    with open(filename, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['submission_id'] == submission_id:
                for key, value in update_fields.items():
                    if key == 'questions' and isinstance(value, list):
                        row[key] = '|'.join(value)
                    elif key == 'evaluation' and isinstance(value, dict):
                        row[key] = str(value)
                    else:
                        row[key] = value
                updated = True
            submissions.append(row)
    # Write back all submissions
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=SUBMISSION_FIELDS)
        writer.writeheader()
        writer.writerows(submissions)
    upload_submissions_to_mongodb()

def upload_assignments_to_mongodb():
    """Upload the contents of assignments.csv to MongoDB."""
    with current_app.app_context():
        mongo_uri = current_app.config['MONGO_URI']
        db_name = current_app.config['DATABASE_NAME']
    try:
        client = MongoClient(mongo_uri)
        db = client[db_name]
        assignments_collection = db['assignments']
        # Clear existing data
        assignments_collection.delete_many({})
        # Load data from CSV
        filename = 'data/assignments.csv'
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                assignments_collection.insert_one(row)
        print("Uploaded assignments to MongoDB")
    except ConnectionFailure as e:
        print(f"Connection to MongoDB failed: {e}")
    except Exception as e:
        print(f"Error uploading assignments to MongoDB: {e}")
    finally:
        client.close()

def upload_submissions_to_mongodb():
    """Upload the contents of submissions.csv to MongoDB."""
    with current_app.app_context():
        mongo_uri = current_app.config['MONGO_URI']
        db_name = current_app.config['DATABASE_NAME']
    try:
        client = MongoClient(mongo_uri)
        db = client[db_name]
        submissions_collection = db['submissions']
        # Clear existing data
        submissions_collection.delete_many({})
        # Load data from CSV
        filename = 'data/submissions.csv'
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                submissions_collection.insert_one(row)
        print("Uploaded submissions to MongoDB")
    except ConnectionFailure as e:
        print(f"Connection to MongoDB failed: {e}")
    except Exception as e:
        print(f"Error uploading submissions to MongoDB: {e}")
    finally:
        client.close()
