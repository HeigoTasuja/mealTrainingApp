from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import get_connection
from blueprints.meal_plans import get_meals_with_macros

ingredients_bp = Blueprint("ingredients", __name__)

@ingredients_bp.route("/", methods=["GET", "POST"])
def manage_ingredients():
    if request.method == "POST":
        name = request.form["name"]
        calories = float(request.form["calories"])
        protein = float(request.form["protein"])
        carbs = float(request.form["carbs"])
        fat = float(request.form["fat"])

        with get_connection() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO ingredients (name, calories, protein, carbs, fat) VALUES (?, ?, ?, ?, ?)",
                (name, calories, protein, carbs, fat)
            )
            conn.commit()

        return redirect(url_for("ingredients.manage_ingredients"))

    with get_connection() as conn:
        ingredients = conn.execute("SELECT * FROM ingredients ORDER BY name").fetchall()

    return render_template("plans/ingredient_reference.html", ingredients=ingredients)


@ingredients_bp.route("/calculate", methods=["POST"])
def calculate_macros():
    name = request.form.get("name", "").strip().lower()
    try:
        grams = float(request.form.get("grams"))
    except (TypeError, ValueError):
        flash("Please enter a valid weight in grams.")
        return redirect(url_for("meal_plans.meal_index"))

    with get_connection() as conn:
        ingredient = conn.execute("SELECT * FROM ingredients WHERE LOWER(name) = ?", (name,)).fetchone()

    if not ingredient:
        flash("Ingredient not found.")
        return render_template("plans/meal_index.html")

    multiplier = grams / 100.0
    result = {
        "name": name,
        "grams": grams,
        "calories": round(ingredient["calories"] * multiplier, 1),
        "protein": round(ingredient["protein"] * multiplier, 1),
        "carbs": round(ingredient["carbs"] * multiplier, 1),
        "fat": round(ingredient["fat"] * multiplier, 1)
    }

    with get_connection() as conn:
        meals = conn.execute("SELECT * FROM meal_plans ORDER BY day").fetchall()

    meals, all_ingredients = get_meals_with_macros()

    return render_template("plans/meal_index.html", ingredient=ingredient, meals=meals, ingredients=all_ingredients, result=result)
