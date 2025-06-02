from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import get_connection

workout_plans_bp = Blueprint("workout_plans", __name__, url_prefix="/plans")

@workout_plans_bp.route("/")
def plans_index():
    with get_connection() as conn:
        exercises = conn.execute("SELECT * FROM exercises").fetchall()
    return render_template("plans/index.html", exercises=exercises)

@workout_plans_bp.route("/add_exercise", methods=["POST"])
def add_exercise():
    name        = request.form.get("name")
    description = request.form.get("description")
    day         = request.form.get("day")      #  Monday … Friday
    category    = request.form.get("category") #  Strength / Mobility

    if not all([name, day, category]):
        flash("Name, day and category are required.")
        return redirect(url_for("workout_plans.plans_index"))

    with get_connection() as conn:
        conn.execute(
            "INSERT INTO exercises (name, description, day, category) VALUES (?,?,?,?)",
            (name, description, day, category)
        )
        conn.commit()
    return redirect(url_for("workout_plans.plans_index"))

@workout_plans_bp.route("/exercise/<int:exercise_id>/delete", methods=["POST"])
def delete_exercise(exercise_id):
    with get_connection() as conn:
        conn.execute("DELETE FROM exercises WHERE id = ?", (exercise_id,))
        conn.commit()
    return redirect(url_for("workout_plans.plans_index"))
