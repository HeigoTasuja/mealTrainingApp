from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import get_connection

meal_plans_bp = Blueprint("meal_plans", __name__, url_prefix="/meal_plans")

@meal_plans_bp.route("/")
def meals_index():
    with get_connection() as conn:
        meals = conn.execute("SELECT * FROM meal_plans").fetchall()
    return render_template("plans/meal_index.html", meals=meals)

@meal_plans_bp.route("/add", methods=["POST"])
def add_meal():
    name        = request.form.get("name")
    ingredients = request.form.get("ingredients") or None
    calories    = request.form.get("calories") or None
    day         = request.form.get("day")
    meal_type   = request.form.get("meal_type")

    if not name or not day or not meal_type:
        flash("Name, day, and meal type are required.")
        return redirect(url_for("meal_plans.meals_index"))

    with get_connection() as conn:
        conn.execute(
            "INSERT INTO meal_plans (name, ingredients, calories, day, meal_type) VALUES (?, ?, ?, ?, ?)",
            (name, ingredients, calories, day, meal_type)
        )
        conn.commit()
    return redirect(url_for("meal_plans.meals_index"))

@meal_plans_bp.route("/delete/<int:meal_id>", methods=["POST"])
def delete_meal(meal_id):
    with get_connection() as conn:
        conn.execute("DELETE FROM meal_plans WHERE id = ?", (meal_id,))
        conn.commit()
    return redirect(url_for("meal_plans.meals_index"))
