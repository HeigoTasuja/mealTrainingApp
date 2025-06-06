from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime
from database import get_connection

workouts_bp = Blueprint("workouts", __name__, url_prefix="/workouts")

@workouts_bp.route("/new", methods=["GET", "POST"])
def log_workout():
    from_day = request.args.get("from_day")
    prefill_exercises = ""

    if from_day:
        with get_connection() as conn:
            rows = conn.execute("""
                SELECT name, description FROM exercises
                WHERE day = ?
            """, (from_day,)).fetchall()

        prefill_exercises = "\n".join(f"{row['name']} — {row['description']}" for row in rows)

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

    default_date = datetime.now().strftime("%Y-%m-%d")
    return render_template("log_workout.html", default_date=default_date, prefill_exercises=prefill_exercises)

@workouts_bp.route("/history")
def workout_history():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM workouts ORDER BY date DESC, id DESC"
        ).fetchall()
    return render_template("workout_history.html", workouts=rows)
