from flask import Flask, render_template, url_for, request, jsonify, redirect, flash, session as flask_session
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import datetime
import re

from models.user_model import Base as UserBase, User
from models.workout_model import Base as WorkoutBase, Workout, Exercise
from models.meal_model import Base as MealBase

app = Flask(__name__)
app.secret_key = "nicolorenzi"

engine = create_engine("sqlite:///users.db", echo=True)

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PASSWORD_REQUIREMENTS = (
    "Passwords must be 8-64 characters long, include at least one uppercase letter, "
    "one lowercase letter, and one special character."
)
DEFAULT_EMAILS = [
    "nico@coreconnect.com",]
DEFAULT_PASSWORD = "Soccernico9#"

def ensure_users_email_column():
    inspector = inspect(engine)
    if "Users" not in inspector.get_table_names():
        return

    existing_columns = {col["name"] for col in inspector.get_columns("Users")}
    if "email" in existing_columns:
        return
    if "username" not in existing_columns:
        return

    with engine.begin() as conn:
        conn.execute(text('ALTER TABLE "Users" RENAME TO "Users_old"'))
        conn.execute(
            text(
                'CREATE TABLE "Users" ('
                'id INTEGER PRIMARY KEY AUTOINCREMENT, '
                'email VARCHAR NOT NULL UNIQUE, '
                'password VARCHAR NOT NULL'
                ')'
            )
        )
        conn.execute(
            text(
                'INSERT INTO "Users" (id, email, password) '
                'SELECT id, username, password FROM "Users_old"'
            )
        )
        conn.execute(text('DROP TABLE "Users_old"'))

ensure_users_email_column()

UserBase.metadata.create_all(bind=engine)
WorkoutBase.metadata.create_all(bind=engine)
MealBase.metadata.create_all(bind=engine)

def ensure_workout_user_column():
    inspector = inspect(engine)
    if "Workouts" not in inspector.get_table_names():
        return

    existing_columns = {col["name"] for col in inspector.get_columns("Workouts")}
    if "user_id" in existing_columns:
        return

    with engine.begin() as conn:
        conn.execute(text('ALTER TABLE "Workouts" ADD COLUMN user_id INTEGER'))

Session = sessionmaker(bind=engine)
db = Session()

def seed_default_users():
    existing_users = {
        user.email for user in db.query(User).filter(User.email.in_(DEFAULT_EMAILS)).all()
    }

    new_users = []
    for email in DEFAULT_EMAILS:
        if email not in existing_users:
            new_users.append(User(email=email, password=generate_password_hash(DEFAULT_PASSWORD)))

    if not new_users:
        return

    db.add_all(new_users)
    try:
        db.commit()
    except Exception:
        db.rollback()

def is_valid_email(email):
    return bool(EMAIL_REGEX.fullmatch((email or "").strip()))

def is_strong_password(password):
    if not password:
        return False
    if not (8 <= len(password) <= 64):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[^A-Za-z0-9]", password):
        return False
    return True

ensure_workout_user_column()
seed_default_users()


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in flask_session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("main"))
        return f(*args, **kwargs)
    return decorated

def current_user_id():
    return flask_session["user_id"]


@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        email = request.form["email"].strip()
        password = request.form["password"]

        if not is_valid_email(email):
            flash("Please enter a valid email address.", "danger")
            return redirect(url_for("main"))

        user = db.query(User).filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            flask_session["user_id"] = user.id
            flask_session.permanent = True
            return redirect(url_for("dashboard"))

        flash("Invalid credentials. Please try again.", "danger")
        return redirect(url_for("main"))

    return render_template(
        "login.html",
        login_reference=url_for("main"),
        register_reference=url_for("register"),
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"].strip()
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if not is_valid_email(email):
            flash("Please enter a valid email address.", "danger")
            return redirect(url_for("register"))

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("register"))

        if not is_strong_password(password):
            flash(PASSWORD_REQUIREMENTS, "danger")
            return redirect(url_for("register"))

        existing = db.query(User).filter_by(email=email).first()
        if existing:
            flash("That email is already registered.", "danger")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)
        new_user = User(email=email, password=hashed_password)
        db.add(new_user)
        db.commit()

        flask_session["user_id"] = new_user.id
        flask_session.permanent = True
        return redirect(url_for("dashboard"))

    return render_template(
        "register.html",
        register_reference=url_for("register"),
        login_reference=url_for("main"),
        password_requirements=PASSWORD_REQUIREMENTS,
    )


@app.route("/logout")
@login_required
def logout():
    flask_session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("main"))


@app.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    return render_template(
        "dashboard.html",
        calorie_calculator_reference=url_for("calculator"),
        workout_tracker_reference=url_for("workout"),
        nutrition_tracker_reference=url_for("nutrition_tracker"),
        progress_tracker_reference=url_for("progress_tracker"),
    )


@app.route("/calorie-calculator", methods=["GET"])
@login_required
def calculator():
    return render_template("calorie-calculator.html")


@app.route("/nutrition-tracker", methods=["GET"])
@login_required
def nutrition_tracker():
    return render_template("nutrition-tracker.html")


@app.route("/workout-tracker", methods=["GET", "POST"])
@login_required
def workout():
    user_id = current_user_id()

    if request.method == "POST":
        exercise_name = request.form["exercise"]
        reps = request.form["repetitions"]
        exercise_weight = request.form["weight"]
        intensity_level = request.form["intensity"]

        exercise = Exercise(
            name=exercise_name,
            repetitions=reps,
            weight=exercise_weight,
            intensity=intensity_level
        )

        date = datetime.date.today()
        workout_entry = db.query(Workout).filter_by(date=date, user_id=user_id).first()
        if not workout_entry:
            workout_entry = Workout(date=date, user_id=user_id)
            db.add(workout_entry)

        workout_entry.exercises.append(exercise)

        try:
            db.commit()
            return redirect(url_for("dashboard"))
        except Exception as e:
            db.rollback()
            return "There was an issue adding your workout", 500

    return render_template("workout-tracker.html")


@app.route("/progress-tracker", methods=["GET"])
@login_required
def progress_tracker():
    return render_template("progress-tracker.html")


@app.route("/api/workouts", methods=["GET"])
@login_required
def get_workouts():
    user_id = current_user_id()
    workouts = (
        db.query(Workout)
        .filter_by(user_id=user_id)
        .order_by(Workout.date.desc())
        .all()
    )
    return jsonify([w.to_dict() for w in workouts])


if __name__ == "__main__":
    app.run(debug=True)
