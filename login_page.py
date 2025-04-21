from flask import Flask, render_template, url_for, request, jsonify, redirect, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.user_model import Base, User
from models.workout_model import Base, Workout, Exercise
import datetime

app = Flask(__name__)
app.secret_key = "pass"
engine = create_engine("sqlite:///users.db", echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

@app.route("/", methods=["GET"])
def main():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = session.query(User).filter_by(username=username, password=password).first()

        if user:
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials. Please try again.", "danger")
            return redirect(url_for("login"))

    return render_template("login.html", login_reference=url_for("login"))

@app.route("/dashboard", methods=["GET"])
def dashboard():
    return render_template("dashboard.html", calorie_calculator_reference=url_for("calculator"), workout_tracker_reference=url_for("workout"))

@app.route("/calorie-calculator", methods=["GET"])
def calculator():
    return render_template("calorie-calculator.html")

@app.route("/workout-tracker", methods=["GET", "POST"])
def workout():
    if (request.method == "POST"):
        exercise_name = request.form["exercise"]
        reps = request.form['repetitions']
        exercise_weight = request.form['weight']
        intensity_level = request.form['intensity']

        exercise = Exercise(name=exercise_name, 
                            repetitions=reps,
                            weight=exercise_weight,
                            intensity=intensity_level)
        
        date = datetime.date.today()
        workout = session.query(Workout).filter_by(date=date).first()
        if not (workout):
            workout = Workout(date=date)
            session.add(workout)

        workout.exercises.append(exercise)

        try: 
            session.commit()
            return redirect(url_for("dashboard"))
        except:
            return 'There was an issue adding your workout'


    return render_template("workout-tracker.html")

if __name__ == "__main__":
    app.run(debug=True)