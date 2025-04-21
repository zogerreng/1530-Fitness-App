from flask import Flask, render_template, url_for, request, jsonify, redirect, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.user_model import Base, User

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

@app.route("/workout-tracker", methods=["GET"])
def workout():
    return render_template("workout-tracker.html")

if __name__ == "__main__":
    app.run(debug=True)