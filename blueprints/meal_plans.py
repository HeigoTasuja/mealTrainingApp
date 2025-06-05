from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import get_connection

meal_plans_bp = Blueprint("meal_plans", __name__, url_prefix="/meal_plans")

# Helper function
def get_meals_with_macros():
    with get_connection() as conn:
        meals = conn.execute("SELECT * FROM meal_plans").fetchall()
        all_ingredients = conn.execute("SELECT * FROM ingredients").fetchall()
        ingredient_map = {i["id"]: i for i in all_ingredients}

        meal_data = []
        for m in meals:
            m_id = m["id"]
            mi_rows = conn.execute("""
                SELECT * FROM meal_ingredients WHERE meal_id = ?
            """, (m_id,)).fetchall()

            total = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}
            ingredients = []

            for mi in mi_rows:
                ing = ingredient_map.get(mi["ingredient_id"])
                if ing:
                    multiplier = mi["grams"] / 100
                    ingredients.append({
                        "name": ing["name"],
                        "grams": mi["grams"],
                        "calories": round(ing["calories"] * multiplier, 1),
                        "protein": round(ing["protein"] * multiplier, 1),
                        "carbs": round(ing["carbs"] * multiplier, 1),
                        "fat": round(ing["fat"] * multiplier, 1)
                    })

                    total["calories"] += ing["calories"] * multiplier
                    total["protein"] += ing["protein"] * multiplier
                    total["carbs"] += ing["carbs"] * multiplier
                    total["fat"] += ing["fat"] * multiplier

            m_dict = dict(m)
            m_dict["ingredients"] = ingredients
            m_dict["totals"] = {k: round(v, 1) for k, v in total.items()}
            meal_data.append(m_dict)

        return meal_data, all_ingredients

@meal_plans_bp.route("/")
def meals_index():
    meals, ingredients = get_meals_with_macros()
    return render_template("plans/meal_index.html", meals=meals, ingredients=ingredients)

@meal_plans_bp.route("/add", methods=["POST"])
def add_meal():
    name = request.form.get("name")
    day = request.form.get("day")
    meal_type = request.form.get("meal_type")

    if not name or not day or not meal_type:
        flash("Name, day, and meal type are required.")
        return redirect(url_for("meal_plans.meals_index"))

    ingredient_names = request.form.getlist("ingredient_name")
    ingredient_grams = request.form.getlist("ingredient_grams")

    with get_connection() as conn:
        # Step 1: Insert the meal
        cursor = conn.execute(
            "INSERT INTO meal_plans (name, day, meal_type) VALUES (?, ?, ?)",
            (name, day, meal_type)
        )
        meal_id = cursor.lastrowid

        # Step 2: Add ingredients (if any)
        for name, grams in zip(ingredient_names, ingredient_grams):
            ingredient = conn.execute(
                "SELECT id FROM ingredients WHERE LOWER(name) = LOWER(?)",
                (name.strip(),)
            ).fetchone()

            if ingredient:
                conn.execute(
                    "INSERT INTO meal_ingredients (meal_id, ingredient_id, grams) VALUES (?, ?, ?)",
                    (meal_id, ingredient["id"], grams)
                )

        conn.commit()

    return redirect(url_for("meal_plans.meals_index"))

@meal_plans_bp.route("/add_ingredient", methods=["POST"])
def add_ingredient():
    meal_id = request.form.get("meal_id")
    ingredient_id = request.form.get("ingredient_id")
    grams = request.form.get("grams")

    if not meal_id or not ingredient_id or not grams:
        flash("All fields required")
        return redirect(url_for("meal_plans.meals_index"))

    with get_connection() as conn:
        conn.execute("""
            INSERT INTO meal_ingredients (meal_id, ingredient_id, grams)
            VALUES (?, ?, ?)
        """, (meal_id, ingredient_id, grams))
        conn.commit()

    return redirect(url_for("meal_plans.meals_index"))

@meal_plans_bp.route("/delete/<int:meal_id>", methods=["POST"])
def delete_meal(meal_id):
    with get_connection() as conn:
        conn.execute("DELETE FROM meal_plans WHERE id = ?", (meal_id,))
        conn.execute("DELETE FROM meal_ingredients WHERE meal_id = ?", (meal_id,))
        conn.commit()
    return redirect(url_for("meal_plans.meals_index"))
