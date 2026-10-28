
from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app import db
from models import Exercise
from schemas import ExerciseSchema

exercise_bp = Blueprint("exercises", __name__, url_prefix="/exercises")

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)


@exercise_bp.route("", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.order_by(Exercise.id).all()
    return jsonify(exercises_schema.dump(exercises)), 200


@exercise_bp.route("/<int:exercise_id>", methods=["GET"])
def get_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return jsonify({"error": "Exercise not found"}), 404

    return jsonify(exercise_schema.dump(exercise)), 200


@exercise_bp.route("", methods=["POST"])
def create_exercise():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "A JSON object is required"}), 400

    try:
        validated_data = exercise_schema.load(data)
    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400

    exercise = Exercise(
        name=validated_data["name"],
        category=validated_data["category"],
        description=validated_data["description"]
    )

    try:
        db.session.add(exercise)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "An exercise with that name already exists"}), 409
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Unable to create exercise"}), 500

    return jsonify(exercise_schema.dump(exercise)), 201


@exercise_bp.route("/<int:exercise_id>", methods=["DELETE"])
def delete_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return jsonify({"error": "Exercise not found"}), 404

    try:
        db.session.delete(exercise)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Unable to delete exercise"}), 500

    return jsonify({"message": "Exercise deleted successfully"}), 200
