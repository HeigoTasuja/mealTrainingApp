from flask import Blueprint, render_template

refeed_bp = Blueprint("refeed", __name__, url_prefix="/refeed")


@refeed_bp.route("/")
def refeed():
    meals = [
        {
            "meal": "White rice (150g) + lean ground beef (150g)",
            "protein": 40,
            "carbs": 60,
            "fat": 15,
        },
        {
            "meal": "Oats (60g) + whey protein (30g) + blueberries (50g)",
            "protein": 35,
            "carbs": 50,
            "fat": 18,
        },
        {
            "meal": "Sweet potato (200g) + grilled salmon (150g)",
            "protein": 45,
            "carbs": 55,
            "fat": 20,
        },
        {
            "meal": "Egg whites (200g) + banana (120g) + peanut butter (10g)",
            "protein": 30,
            "carbs": 35,
            "fat": 10,
        },
        {
            "meal": "Greek yogurt (200g) + honey (15g) + granola (40g)",
            "protein": 25,
            "carbs": 45,
            "fat": 8,
        },
    ]
    return render_template("refeed.html", meals=meals)
