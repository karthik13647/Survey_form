from flask import Flask, request, jsonify, render_template
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'survey.db'

def init_db():
    """Initialize the SQLite database if it doesn't exist."""
    if not os.path.exists(DATABASE):
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS responses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    gender TEXT NOT NULL
                )
            """)
            conn.commit()

def save_response(gender):
    """Save the survey response to the database."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO responses (gender) VALUES (?)", (gender,))
        conn.commit()

def get_survey_response(gender):
    """Return a dynamic message based on the selected gender."""
    if gender == "male":
        return {
            "message": "How is your day, sir? Unfortunately, this research is not for you. Go check your Insta feed; you might find something good!"
        }
    elif gender == "female":
        return {
            "message": "Great! We are conducting a research survey. Let's get started!"
        }
    elif gender == "teen_female":
        return {
            "message": "How was your day, cutie? Let's get started!"
        }
    elif gender == "old_female":
        return {
            "message": "How is your day going so far, angel? Let's begin the survey!"
        }
    else:
        return {
            "message": "Invalid choice. Please try again."
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/survey', methods=['POST'])
def survey():
    data = request.get_json()
    gender = data.get("gender", "").lower()
    save_response(gender)
    response = get_survey_response(gender)
    return jsonify(response)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
