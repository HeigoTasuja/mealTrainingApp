from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime
from database import get_connection

meals_bp = Blueprint("meals", __name__, url_prefix="/meals")

@meals_bp.route("/new", methods=["GET", "POST"])
def log_meal():
    from_meal_id = request.args.get("from_meal_id")
    prefill_data = None

    if from_meal_id:
        with get_connection() as conn:
            meal = conn.execute("SELECT * FROM meal_plans WHERE id = ?", (from_meal_id,)).fetchone()
            meal_ingredients = conn.execute("""
                SELECT i.name, mi.grams, i.calories, i.protein, i.carbs, i.fat
                FROM meal_ingredients mi
                JOIN ingredients i ON mi.ingredient_id = i.id
                WHERE meal_id = ?
            """, (from_meal_id,)).fetchall()

        total_protein = sum((ing["protein"] * ing["grams"] / 100) for ing in meal_ingredients)
        total_carbs = sum((ing["carbs"] * ing["grams"] / 100) for ing in meal_ingredients)
        total_fat = sum((ing["fat"] * ing["grams"] / 100) for ing in meal_ingredients)

        prefill_data = {
            "description": meal["name"],
            "protein": round(total_protein, 1),
            "carbs": round(total_carbs, 1),
            "fat": round(total_fat, 1)
        }

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
    return render_template("log_meal.html", default_date=default_date, prefill=prefill_data)

@meals_bp.route("/history")
def meal_history():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM meals ORDER BY date DESC, id DESC"
        ).fetchall()
    return render_template("meal_history.html", meals=rows)
