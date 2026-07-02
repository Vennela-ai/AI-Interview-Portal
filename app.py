

from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from gemini_service import generate_questions, evaluate_answers
from models import User, InterviewResult, db
import re

app = Flask(__name__)
app.secret_key = "your_secret_key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            return redirect(url_for("dashboard"))

        return "Invalid Email or Password!"

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return "Email already registered!"

        new_user = User(
            name=name,
            email=email,
            password=password
        )

        db.session.add(new_user)
        db.session.commit()

        return "Registration Successful!"

    return render_template("register.html")
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    interviews = InterviewResult.query.filter_by(
        user_id=session["user_id"]
    ).all()

    total_interviews = len(interviews)

    if total_interviews > 0:
        average_score = round(
            sum(i.score for i in interviews) / total_interviews,
            2
        )
        highest_score = max(i.score for i in interviews)
    else:
        average_score = 0
        highest_score = 0

    recent = InterviewResult.query.filter_by(
        user_id=session["user_id"]
    ).order_by(
        InterviewResult.interview_date.desc()
    ).limit(5).all()

    return render_template(
        "dashboard.html",
        user=user,
        total_interviews=total_interviews,
        average_score=average_score,
        highest_score=highest_score,
        recent=recent
    )
@app.route("/interview/setup")
def interview_setup():
    return render_template("interview_setup.html")
@app.route("/submit-interview", methods=["POST"])
def submit_interview():

    questions = []
    answers = []
    i = 1

    while True:
        question = request.form.get(f"question{i}")
        answer = request.form.get(f"answer{i}")

        if not question:
            break

        questions.append(question)
        answers.append(answer)
        i += 1

    result = evaluate_answers(
        "\n".join(questions),
        "\n".join(answers)
    )

    score = 0

    match = re.search(r"Overall Score:\s*(\d+(\.\d+)?)/100", result)

    if match:
        score = float(match.group(1))

    if "user_id" in session:
        interview = InterviewResult(
            user_id=session["user_id"],
            interview_type="AI Mock Interview",
            score=score,
            feedback=result
        )

        db.session.add(interview)
        db.session.commit()

    return render_template(
        "result.html",
        result=result
    )
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
@app.route("/interview")
def interview():
    questions = [
        "Tell me about yourself.",
        "What are your strengths?",
        "Why should we hire you?",
        "Describe a challenging project you worked on.",
        "Where do you see yourself in five years?"
    ]

    return render_template("interview.html", questions=questions)
@app.route("/generate-questions", methods=["POST"])
def interview_questions():

    role = request.form["role"]
    experience = request.form["experience"]
    skills = request.form["skills"]
    difficulty = request.form["difficulty"]
    interview_type = request.form["interview_type"]
    question_count = request.form["question_count"]

    response = generate_questions(
        role,
        experience,
        skills,
        difficulty,
        interview_type,
        question_count
    )

    questions = []

    for line in response.split("\n"):

        line = line.strip()

        if line:
            questions.append(line)
    session["questions"] = questions

    return render_template(
        "interview.html",
        questions=questions
    )
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/login')

    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user)
@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        # Check current password
        if not check_password_hash(user.password, current_password):
            flash('Current password is incorrect!', 'danger')
            return redirect(url_for('change_password'))

        # Check if new passwords match
        if new_password != confirm_password:
            flash('New passwords do not match!', 'danger')
            return redirect(url_for('change_password'))

        # Save new password
        user.password = generate_password_hash(new_password)
        db.session.commit()

        flash('Password changed successfully!', 'success')
        return redirect(url_for('profile'))

    return render_template('change_password.html')
@app.route("/history")
def history():

    if "user_id" not in session:
        return redirect(url_for("login"))

    results = InterviewResult.query.filter_by(
        user_id=session["user_id"]
    ).order_by(
        InterviewResult.interview_date.desc()
    ).all()

    return render_template(
        "history.html",
        results=results
    )
@app.route("/submit_answers", methods=["POST"])
def submit_answers():

    if "user_id" not in session:
        return redirect(url_for("login"))

    questions = session.get("questions")

    if not questions:
        flash("Interview session expired. Please generate questions again.", "warning")
        return redirect(url_for("interview_setup"))

    answers = []

    for i in range(len(questions)):
        answers.append(request.form.get(f"answer{i+1}", "").strip())

    # Get AI Evaluation
    result = evaluate_answers(questions, answers)
    result = result.replace("# Overall Score", "<h3>🏆 Overall Score</h3>")
    result = result.replace("# Technical Skills", "<h3>💻 Technical Skills</h3>")
    result = result.replace("# Communication", "<h3>🗣 Communication</h3>")
    result = result.replace("# Strengths", "<h3>⭐ Strengths</h3>")
    result = result.replace("# Areas to Improve", "<h3>⚠️ Areas to Improve</h3>")
    result = result.replace("# Focus Next", "<h3>🎯 Focus Next</h3>")
    result = result.replace("# Final Verdict", "<h3>✅ Final Verdict</h3>")

    result = result.replace("\n", "<br>")

    # Extract Score
    score = 0

    match = re.search(r"Overall Score:\s*(\d+(\.\d+)?)/100", result)

    if match:
        score = float(match.group(1))

    # Save Interview Result
    interview = InterviewResult(
        user_id=session["user_id"],
        interview_type="AI Mock Interview",
        score=score,
        feedback=result
    )

    db.session.add(interview)
    db.session.commit()

    return render_template(
        "result.html",
        result=result,
        score=score
    )
if __name__ == "__main__":
    app.run(debug=True)