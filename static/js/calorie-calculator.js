//Calories Calculator is part of tracker

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("calorieForm");
    const result = document.getElementById("result");

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const weight = parseFloat(document.getElementById("weight").value);
        const height = parseFloat(document.getElementById("height").value);
        const age = parseFloat(document.getElementById("age").value);
        const gender = document.getElementById("gender").value;
        const activityLevel = parseFloat(document.getElementById("activity").value);

        let bmr;

        if (gender === "male") {
            bmr = 10 * weight + 6.25 * height - 5 * age + 5;
        } else {
            bmr = 10 * weight + 6.25 * height - 5 * age - 161;
        }

        const dailyCalories = bmr * activityLevel;
        result.textContent = `Your estimated daily calorie requirement is: ${Math.round(dailyCalories)} kcal`;
    });
});
