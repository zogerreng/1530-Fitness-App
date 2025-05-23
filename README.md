# Core Connect 
CoreConnect is a comprehensive fitness application designed to help users monitor their caloric intake, track workouts, and achieve their health goals efficiently, keeping the user motivated and consistent.

---

##  Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)

---

##  Features

- **Caloric Calculator*: Track daily caloric intake goals for each body type.
- **Workout Tracker**: Log workouts with details like type, duration, and calories burned.
- **Nutrition Tracker**: Record meals and snacks to monitor calorie consumption.
- **Progress Tracker**: View graphs and statistics to track progress over time.

---

##  Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/zogerreng/1530-Fitness-App.git
   cd 1530-Fitness-App

2. **Create a virtual environment (needs to be done only once):**
   ```bash
   python -m venv venv

3. **Activate virtual environment:**
   ```bash
   In Mac OS:      source venv/bin/activate
   In Windows:     .\venv\Scripts\activate 

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   
3. **Run the App:**
   ```bash
   python login_page.py

4. **Copy and paste the link they give into a browser:**
   ```bash
   ex. http://127.0.0.1:5000

5. To login, use any of these usernames with the password "pass":
   - nico
   - devansh
   - roger
   - michael
   - maggie

##  Technologies Used
   - Frontend: HTML, CSS, JavaScript
   
   - Backend: Flask (Python)
   
   - Database: SQLite

## Contributing 
Pull requests are welcome! To contribute:

   - Fork the repository

   - Create a new branch

   - Make your changes

   - Submit a pull request

## Testing 
   - Run App from terminal
   - on a different terminal envoke selinium web testing by
   ```bash
      python -m unittest tests/test_calorie_calculator.py
