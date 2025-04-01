from flask import Flask, request, jsonify, render_template, flash, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Required for flash messages
DATABASE = 'survey.db'

def init_db():
    """Initialize the SQLite database if it doesn't exist."""
    if not os.path.exists(DATABASE):
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS responses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    gender TEXT NOT NULL,
                    day_response TEXT
                )
            """)
            conn.commit()

def save_response(gender):
    """Save the gender response and return the record ID."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO responses (gender) VALUES (?)", (gender,))
        conn.commit()
        return cursor.lastrowid

def update_day_response(record_id, day_response):
    """Update the record with the day response."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE responses SET day_response=? WHERE id=?", (day_response, record_id))
        conn.commit()

def get_survey_response(gender):
    """Return a dynamic message based on the selected gender."""
    if gender == "male":
        return {
            "message": "How is your day, sir? Unfortunately, this research is not for you. Go check your Insta feed; you might find something good!"
        }
    elif gender == "female":
        return {
            "message": "How is your day? Please tell us how your day has been."
        }
    elif gender == "teen_female":
        return {
            "message": "How is your day? Let us know how it went, cutie."
        }
    elif gender == "old_female":
        return {
            "message": "How is your day? We'd love to hear about your day."
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
    record_id = save_response(gender)
    response = get_survey_response(gender)
    # For non-male genders, include a redirect to the follow-up question page
    if gender != "male":
        response["redirect"] = "/day?rid=" + str(record_id)
    return jsonify(response)

@app.route('/day', methods=['GET', 'POST'])
def day():
    if request.method == 'GET':
        # Display the follow-up question page with the record id
        record_id = request.args.get("rid")
        return render_template('day.html', record_id=record_id)
    else:
        # Process the day response submission
        record_id = request.form.get("record_id")
        day_response = request.form.get("day_response")
        update_day_response(record_id, day_response)
        flash("Your response has been recorded!")
        # Redirect back to the same page with the record id to show the flash message
        return redirect(url_for('day', rid=record_id))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
