from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime
from database import get_connection

meals_bp = Blueprint("meals", __name__, url_prefix="/meals")


@meals_bp.route("/new", methods=["GET", "POST"])
def log_meal():
    if request.method == "POST":
        data = (
            request.form["date"],
            request.form["meal_time"],
            request.form["description"],
            float(request.form["protein"]),
            float(request.form["carbs"]),
            float(request.form["fat"]),
            request.form["fasted"],
        )
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO meals (date, meal_time, description, protein, carbs, fat, fasted) VALUES (?, ?, ?, ?, ?, ?, ?)",
                data,
            )
            conn.commit()
        return redirect(url_for("index"))

    default_date = datetime.now().strftime("%Y-%m-%d")
    return render_template("log_meal.html", default_date=default_date)
