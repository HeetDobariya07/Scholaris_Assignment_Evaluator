# Assignment Evaluator Platform

A web-based platform for automated assignment submission and evaluation.

---

## 🚀 Overview

This project provides an end-to-end solution for:
- Uploading and managing assignments and submissions
- Evaluating student submissions

---

## 🧑‍💻 Features

- **Student Portal**: Upload assignment submissions.
- **Teacher Portal**: Create assignments, view and evaluate student submissions.
- **MongoDB Integration**: All assignments and submissions are stored in MongoDB for robust data management.

---

## 🗂️ Data

The project manages two main CSV files located in the `/data/` directory:

-   `assignments.csv`: Contains information about the assignments, such as title, description, subject, deadline, and grading criteria.

-   `submissions.csv`: Stores student submissions, including submission ID, assignment ID, student ID, questions, and evaluation data.

Uploaded assignment files are stored in the `/data/assignments/` directory.

---

## 🏗️ Tech Stack

-   **Backend**: Python, Flask
-   **Frontend**: HTML, CSS, Bootstrap, Jinja2, JavaScript
-   **Database**: MongoDB

---

## ⚙️ Setup Instructions

1.  **Clone the Repository**
    ```
    git clone https://github.com/yourusername/assignment-evaluator.git
    cd assignment-evaluator
    ```

2.  **Install Dependencies**
    ```
    pip install -r requirements.txt
    ```

3.  **Set Up MongoDB**
    -   Make sure MongoDB is running locally or update `MONGO_URI` and `DATABASE_NAME` in `app.py` for a remote DB.

4.  **Configure Environment Variables**
    -   Set your environment variables as needed (e.g., `GROQ_API_KEY` for the Groq API).

5.  **Run the Application**
    ```
    python app.py
    ```
    -   Access the app at `http://localhost:5000/`

---

## 📁 Project Structure
```
Scholaris_Assignment_Evaluator/
├── pycache/
├── data/
│ ├── assignments/
│ ├── assignments.csv
│ └── submissions.csv
├── static/
│ ├── css/
│ │ ├── create_assignment.css
│ │ ├── evaluate_submissions.css
│ │ ├── student_dashboard.css
│ │ ├── student_submit_assignment.css
│ │ ├── student_view_assignments.css
│ │ ├── style.css
│ │ ├── submissions.css
│ │ └── teacher_dashboard.css
│ └── js/
│ └── script.js
├── templates/
│ ├── student/
│ │ ├── dashboard.html
│ │ ├── submit_assignment.html
│ │ └── view_assignments.html
│ ├── teacher/
│ │ ├── create_assignment.html
│ │ ├── dashboard.html
│ │ ├── evaluate_submission.html
│ │ └── view_submissions.html
│ └── index.html
├── uploads/
├── app.py
├── extractor.py
├── groq_handler.py
├── README.md
└── utils.py
```
---

## 🤝 Contributing

Pull requests and feature suggestions are welcome! Please open an issue or submit a PR.

---

## 📬 Contact

For questions or support, open an issue or contact heetdobariya07@gmail.com / devanshidudhatra77@gmail.com.
