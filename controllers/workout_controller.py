
from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app import db
from models import Workout, Exercise, WorkoutExercise
from schemas import WorkoutSchema

workout_bp = Blueprint("workouts", __name__, url_prefix="/workouts")

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)


@workout_bp.route("", methods=["GET"])
def get_workouts():
    workouts = Workout.query.order_by(Workout.id).all()
    return jsonify(workouts_schema.dump(workouts)), 200


@workout_bp.route("/<int:workout_id>", methods=["GET"])
def get_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return jsonify({"error": "Workout not found"}), 404

    return jsonify(workout_schema.dump(workout)), 200


@workout_bp.route("", methods=["POST"])
def create_workout():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "A JSON object is required"}), 400

    try:
        validated_data = workout_schema.load(data)
    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400

    workout = Workout(
        name=validated_data["name"],
        description=validated_data["description"]
    )

    try:
        db.session.add(workout)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "A workout with that name already exists"}), 409
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Unable to create workout"}), 500

    return jsonify(workout_schema.dump(workout)), 201


@workout_bp.route("/<int:workout_id>", methods=["DELETE"])
def delete_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return jsonify({"error": "Workout not found"}), 404

    try:
        db.session.delete(workout)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Unable to delete workout"}), 500

    return jsonify({"message": "Workout deleted successfully"}), 200


@workout_bp.route("/<int:workout_id>/exercises", methods=["POST"])
def add_exercise(workout_id):
    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return jsonify({"error": "Workout not found"}), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "A JSON object is required"}), 400

    try:
        validated_data = workout_schema.fields["workout_exercises"].inner.load(data)
    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400

    exercise = db.session.get(Exercise, validated_data["exercise_id"])

    if exercise is None:
        return jsonify({"error": "Exercise not found"}), 404

    existing = WorkoutExercise.query.filter_by(
        workout_id=workout_id,
        exercise_id=exercise.id
    ).first()

    if existing:
        return jsonify({"error": "Exercise already belongs to this workout"}), 409

    association = WorkoutExercise(
        workout=workout,
        exercise=exercise,
        sets=validated_data.get("sets"),
        reps=validated_data.get("reps"),
        duration=validated_data.get("duration")
    )

    try:
        db.session.add(association)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Duplicate or invalid workout exercise"}), 409
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Unable to add exercise"}), 500

    return jsonify(workout_schema.dump(workout)), 201
