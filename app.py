import os
import uuid
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from werkzeug.utils import secure_filename
import csv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from extractor import (
    extract_text,
    allowed_file
)
from utils import load_assignments, save_assignment, save_submission, update_submission
from groq_handler import generate_evaluation_questions

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for session management

app.config['MONGO_URI'] = 'mongodb+srv://heetdobariya07:uDR0Eeztg9NllZUy@cluster.yn4nj.mongodb.net/resume_analyzer?retryWrites=true&w=majority'  # Replace with your MongoDB URI
app.config['DATABASE_NAME'] = 'assignment_db'

try:
    client = MongoClient(app.config['MONGO_URI'])
    db = client[app.config['DATABASE_NAME']]
    client.admin.command('ping')
    print("Connected to MongoDB")
except ConnectionFailure as e:
    print(f"Connection to MongoDB failed: {e}")
    db = None

app.config['UPLOAD_FOLDER'] = 'data/assignments'
app.config['ASSIGNMENTS_FILE'] = 'data/assignments.csv'
app.config['SUBMISSIONS_FILE'] = 'data/submissions.csv'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'txt'}

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('data', exist_ok=True)

# Initialize assignments (load from CSV)
assignments = load_assignments(app.config['ASSIGNMENTS_FILE'])

# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/teacher')
def teacher_dashboard():
    return render_template('teacher/dashboard.html', assignments=assignments)

@app.route('/student')
def student_dashboard():
    return render_template('student/dashboard.html', assignments=assignments)

@app.route('/teacher/create_assignment', methods=['GET', 'POST'])
def create_assignment():
    if request.method == 'POST':
        assignment_id = str(uuid.uuid4())
        assignment_data = {
            'assignment_id': assignment_id,
            'title': request.form['title'],
            'description': request.form['description'],
            'subject': request.form['subject'],
            'deadline': request.form['deadline'],
            'grading_criteria': request.form['criteria']
        }
        save_assignment(app.config['ASSIGNMENTS_FILE'], assignment_data)
        assignments[assignment_id] = assignment_data
        return redirect(url_for('teacher_dashboard'))
    return render_template('teacher/create_assignment.html')

@app.route('/student/view_assignments/<assignment_id>')
def view_assignment(assignment_id):
    assignment = next((a for id, a in assignments.items() if id == assignment_id), None)
    if assignment:
        return render_template('student/view_assignments.html', assignment=assignment)
    else:
        return "Assignment not found"  # Or redirect to an error page

@app.route('/student/submit_assignment/<assignment_id>', methods=['POST'])
def submit_assignment(assignment_id):
    # if 'user_id' not in session:
    #     return redirect(url_for('login'))  # Redirect to login if not logged in
    student_id = "test_student"

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            file.save(filepath)
            assignment_text = extract_text(filepath)
            evaluation_questions = generate_evaluation_questions(assignment_text)

            if not evaluation_questions:
                return jsonify({'error': 'Could not generate evaluation questions'}), 500

            submission_data = {
                'submission_id': str(uuid.uuid4()),
                'assignment_id': assignment_id,
                'student_id': student_id,
                'questions': evaluation_questions,
                'evaluation': {}
            }
            save_submission(app.config['SUBMISSIONS_FILE'], submission_data)

            return jsonify({
                'submission_id': submission_data['submission_id'],
                'questions': evaluation_questions
            })

        except Exception as e:
            return jsonify({'error': str(e)}), 500
        # finally:
        #     if os.path.exists(filepath):
        #         os.remove(filepath)

    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/teacher/evaluate/<submission_id>', methods=['POST'])
def evaluate_submission(submission_id):
    evaluation_data = request.json
    update_submission(
        app.config['SUBMISSIONS_FILE'],
        submission_id,
        {'evaluation': evaluation_data}
    )
    return jsonify({'status': 'success'})

@app.route('/teacher/view_submissions/<assignment_id>')
def view_submissions(assignment_id):
    submissions = []
    with open(app.config['SUBMISSIONS_FILE'], 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['assignment_id'] == assignment_id:
                submissions.append(row)

    assignment = next((a for id, a in assignments.items() if id == assignment_id), None)
    if not assignment:
        return "Assignment not found"
    return render_template('teacher/view_submissions.html', submissions=submissions, assignment=assignment)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# --- Main ---
if __name__ == '__main__':
    app.run(debug=True)