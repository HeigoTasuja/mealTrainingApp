from flask import Flask, render_template, url_for, redirect
from datetime import datetime

from database import init_db
from blueprints.workouts import workouts_bp
from blueprints.meals import meals_bp
from blueprints.refeed import refeed_bp
from blueprints.workout_plans import workout_plans_bp
from blueprints.meal_plans import meal_plans_bp


def create_app():
    app = Flask(__name__)

    app.secret_key = "9aysd9yas97tyvadsiuyf9asfauyv98asy9" # :TODO update nad place somewhere secure and replace with variable

    # Initialize the SQLite DB and ensure tables exist
    init_db()

    # Register Blueprints
    app.register_blueprint(workouts_bp)
    app.register_blueprint(meals_bp)
    app.register_blueprint(refeed_bp)
    app.register_blueprint(workout_plans_bp)
    app.register_blueprint(meal_plans_bp)

    # Root route
    @app.route("/")
    def index():
        today = datetime.now().strftime("%Y-%m-%d")
        return render_template("index.html", today=today)

    # Shortcuts to workout and meals
    @app.route('/log-workout')
    def shortcut_workout():
        return redirect(url_for('workouts.log_workout'))

    @app.route('/log-meal')
    def shortcut_meal():
        return redirect(url_for('meals.log_meal'))

    return app


if __name__ == "__main__":
    flask_app = create_app()
    # 0.0.0.0 allows connections from local network (iPhone)
    flask_app.run(debug=True, host="0.0.0.0", port=5000)
