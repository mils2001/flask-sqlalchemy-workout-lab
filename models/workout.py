
from datetime import datetime

from sqlalchemy.orm import validates

from app import db


class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan"
    )

    exercises = db.relationship(
        "Exercise",
        secondary="workout_exercises",
        viewonly=True
    )

    @validates("name")
    def validate_name(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Workout name cannot be empty.")
        if len(value.strip()) > 100:
            raise ValueError("Workout name cannot exceed 100 characters.")
        return value.strip()

    @validates("description")
    def validate_description(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Workout description cannot be empty.")
        if len(value.strip()) > 255:
            raise ValueError("Workout description cannot exceed 255 characters.")
        return value.strip()

    def __repr__(self):
        return f"<Workout {self.name}>"
