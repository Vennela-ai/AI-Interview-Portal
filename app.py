from flask import Flask, render_template, request, redirect, url_for, flash, session
from gemini_service import generate_questions, evaluate_answers
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db

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
    return render_template("dashboard.html")
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

    response = generate_questions(role, experience, skills)

    questions = []

    for line in response.split("\n"):

        line = line.strip()

        if line:
            questions.append(line)

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
if __name__ == "__main__":
    app.run(debug=True)