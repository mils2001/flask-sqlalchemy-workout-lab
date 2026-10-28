
from datetime import datetime

from sqlalchemy.orm import validates

from app import db


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all, delete-orphan"
    )

    @validates("name")
    def validate_name(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Exercise name cannot be empty.")
        if len(value.strip()) > 100:
            raise ValueError("Exercise name cannot exceed 100 characters.")
        return value.strip()

    @validates("category")
    def validate_category(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Exercise category cannot be empty.")
        if len(value.strip()) > 50:
            raise ValueError("Exercise category cannot exceed 50 characters.")
        return value.strip()

    @validates("description")
    def validate_description(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Exercise description cannot be empty.")
        if len(value.strip()) > 255:
            raise ValueError("Exercise description cannot exceed 255 characters.")
        return value.strip()

    def __repr__(self):
        return f"<Exercise {self.name}>"
