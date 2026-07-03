from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# ---------------- USER ---------------- #

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(100), unique=True, nullable=False)

    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<User {self.name}>"


# ---------------- OVERALL RESULT ---------------- #

class InterviewResult(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )

    interview_type = db.Column(db.String(100))

    score = db.Column(db.Float)

    feedback = db.Column(db.Text)

    interview_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


# ---------------- QUESTION-WISE RESULT ---------------- #

class InterviewAnswer(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    interview_result_id = db.Column(
        db.Integer,
        db.ForeignKey('interview_result.id'),
        nullable=False
    )

    question_number = db.Column(db.Integer)

    question = db.Column(db.Text)

    answer = db.Column(db.Text)

    ai_feedback = db.Column(db.Text)

    marks = db.Column(db.Float)