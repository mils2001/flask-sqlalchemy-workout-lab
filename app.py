
import os

from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError

from config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(
        os.path.join(os.path.dirname(__file__), "instance"),
        exist_ok=True
    )

    db.init_app(app)
    migrate.init_app(app, db)

    from models import Workout, Exercise, WorkoutExercise
    from controllers.workout_controller import workout_bp
    from controllers.exercise_controller import exercise_bp

    app.register_blueprint(workout_bp, url_prefix="/api/workouts")
    app.register_blueprint(exercise_bp, url_prefix="/api/exercises")
    

    @app.route("/")
    def home():
        return jsonify({
            "message": "Workout Application API is running"
        })

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return jsonify({"errors": error.messages}), 400

    return app


app = create_app()
