
from app import db


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)

    workout_id = db.Column(
        db.Integer,
        db.ForeignKey("workouts.id", ondelete="CASCADE"),
        nullable=False
    )

    exercise_id = db.Column(
        db.Integer,
        db.ForeignKey("exercises.id", ondelete="CASCADE"),
        nullable=False
    )

    sets = db.Column(db.Integer, nullable=True)
    reps = db.Column(db.Integer, nullable=True)
    duration = db.Column(db.Integer, nullable=True)

    __table_args__ = (
        db.UniqueConstraint(
            "workout_id",
            "exercise_id",
            name="unique_workout_exercise"
        ),
        db.CheckConstraint(
            "sets IS NULL OR sets > 0",
            name="positive_sets"
        ),
        db.CheckConstraint(
            "reps IS NULL OR reps > 0",
            name="positive_reps"
        ),
        db.CheckConstraint(
            "duration IS NULL OR duration > 0",
            name="positive_duration"
        ),
    )

    workout = db.relationship(
        "Workout",
        back_populates="workout_exercises"
    )

    exercise = db.relationship(
        "Exercise",
        back_populates="workout_exercises"
    )

    def __repr__(self):
        return (
            f"<WorkoutExercise workout={self.workout_id} "
            f"exercise={self.exercise_id}>"
        )
