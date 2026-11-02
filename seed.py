
from app import app, db
from models import Workout, Exercise, WorkoutExercise


with app.app_context():
    workouts_data = [
        {
            "name": "Full Body Strength",
            "description": "A complete strength training workout."
        },
        {
            "name": "Cardio Training",
            "description": "A workout focused on cardiovascular fitness."
        },
        {
            "name": "Upper Body Workout",
            "description": "Exercises targeting the upper body."
        }
    ]

    exercises_data = [
        {
            "name": "Push-ups",
            "category": "Strength",
            "description": "An exercise targeting the chest, shoulders and arms."
        },
        {
            "name": "Squats",
            "category": "Strength",
            "description": "A lower body exercise targeting the legs."
        },
        {
            "name": "Jumping Jacks",
            "category": "Cardio",
            "description": "A full body cardiovascular exercise."
        },
        {
            "name": "Plank",
            "category": "Core",
            "description": "An exercise that strengthens the core."
        },
        {
            "name": "Lunges",
            "category": "Strength",
            "description": "An exercise targeting the legs and glutes."
        }
    ]

    workouts = {}
    exercises = {}

    for item in workouts_data:
        workout = Workout.query.filter_by(name=item["name"]).first()

        if workout is None:
            workout = Workout(**item)
            db.session.add(workout)

        workouts[item["name"]] = workout

    for item in exercises_data:
        exercise = Exercise.query.filter_by(name=item["name"]).first()

        if exercise is None:
            exercise = Exercise(**item)
            db.session.add(exercise)

        exercises[item["name"]] = exercise

    db.session.flush()

    associations = [
        ("Full Body Strength", "Push-ups", 3, 12, None),
        ("Full Body Strength", "Squats", 3, 15, None),
        ("Full Body Strength", "Plank", 3, None, 60),
        ("Cardio Training", "Jumping Jacks", 3, 30, None),
        ("Cardio Training", "Lunges", 3, 12, None),
        ("Upper Body Workout", "Push-ups", 4, 10, None),
        ("Upper Body Workout", "Plank", 3, None, 45)
    ]

    for workout_name, exercise_name, sets, reps, duration in associations:
        workout = workouts[workout_name]
        exercise = exercises[exercise_name]

        existing = WorkoutExercise.query.filter_by(
            workout_id=workout.id,
            exercise_id=exercise.id
        ).first()

        if existing is None:
            db.session.add(
                WorkoutExercise(
                    workout=workout,
                    exercise=exercise,
                    sets=sets,
                    reps=reps,
                    duration=duration
                )
            )

    db.session.commit()

    print("Database seeded successfully!")
