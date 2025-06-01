from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime
from database import get_connection

workouts_bp = Blueprint("workouts", __name__, url_prefix="/workouts")


@workouts_bp.route("/new", methods=["GET", "POST"])
def log_workout():
    if request.method == "POST":
        data = (
            request.form["date"],
            request.form["session_type"],
            request.form["body_part"],
            request.form["exercises"],
            request.form["notes"],
        )
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO workouts (date, session_type, body_part, exercises, notes) VALUES (?, ?, ?, ?, ?)",
                data,
            )
            conn.commit()
        return redirect(url_for("index"))

    # Pre‑fill current date for convenience
    default_date = datetime.now().strftime("%Y-%m-%d")
    return render_template("log_workout.html", default_date=default_date)


@workouts_bp.route("/history")
def workout_history():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM workouts ORDER BY date DESC, id DESC"
        ).fetchall()
    return render_template("workout_history.html", workouts=rows)
