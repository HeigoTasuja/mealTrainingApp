
from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import get_connection

workout_plans_bp = Blueprint("workout_plans", __name__, url_prefix="/plans")

@workout_plans_bp.route("/")
def plans_index():
    with get_connection() as conn:
        plans = conn.execute("SELECT * FROM workout_plans").fetchall()
        exercises = conn.execute("SELECT * FROM exercises").fetchall()
    return render_template("plans/index.html",
                           plans=plans,
                           exercises=exercises)

@workout_plans_bp.route("/<category>")
def plans_by_category(category):
    with get_connection() as conn:
        plans = conn.execute(
            "SELECT * FROM workout_plans WHERE category = ?", (category,)
        ).fetchall()
    return render_template("plans/category.html", category=category, plans=plans)

@workout_plans_bp.route("/plan/<int:plan_id>")
def view_plan(plan_id):
    with get_connection() as conn:
        plan = conn.execute("SELECT * FROM workout_plans WHERE id = ?", (plan_id,)).fetchone()
        exercises = conn.execute("SELECT * FROM exercises WHERE plan_id = ?", (plan_id,)).fetchall()
    return render_template("plans/plan_detail.html", plan=plan, exercises=exercises)

@workout_plans_bp.route("/plan/<int:plan_id>/add_exercise", methods=["POST"])
def add_exercise(plan_id):
    name = request.form.get("name")
    description = request.form.get("description")
    if not name:
        flash("Exercise name is required")
        return redirect(url_for("workout_plans.view_plan", plan_id=plan_id))
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO exercises (plan_id, name, description) VALUES (?, ?, ?)",
            (plan_id, name, description)
        )
        conn.commit()
    return redirect(url_for("workout_plans.view_plan", plan_id=plan_id))

@workout_plans_bp.route("/exercise/<int:exercise_id>/delete", methods=["POST"])
def delete_exercise(exercise_id):
    with get_connection() as conn:
        conn.execute("DELETE FROM exercises WHERE id = ?", (exercise_id,))
        conn.commit()
    plan_id = request.form.get("plan_id")
    return redirect(url_for("workout_plans.view_plan", plan_id=plan_id))


@workout_plans_bp.route("/add_plan", methods=["POST"])
def add_plan():
    name = request.form.get("name")
    category = request.form.get("category")
    day = request.form.get("day_of_week")
    plan_type = request.form.get("type")
    body_part = request.form.get("body_part")
    if not name or not day or not category or not body_part:
        flash("All fields are required.")
        return redirect(url_for("workout_plans.plans_index"))

    if not plan_type:
        plan_type = "Strenght" if category == "Strenght" else "Mobility"

    with get_connection() as conn:
        conn.execute(
            "INSERT INTO workout_plans (name, category, day, type, body_part) VALUES (?, ?, ?, ?, ?)",
            (name, category, day, plan_type, body_part),
        )
        conn.commit()
    return redirect(url_for("workout_plans.plans_index"))
