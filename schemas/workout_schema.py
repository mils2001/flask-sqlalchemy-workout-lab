
from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    exercise_id = fields.Int(required=True, strict=True, validate=validate.Range(min=1))
    sets = fields.Int(allow_none=True, load_default=None, validate=validate.Range(min=1))
    reps = fields.Int(allow_none=True, load_default=None, validate=validate.Range(min=1))
    duration = fields.Int(allow_none=True, load_default=None, validate=validate.Range(min=1))


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100, error="Name must contain 1 to 100 characters.")
    )
    description = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=255, error="Description must contain 1 to 255 characters.")
    )
    created_at = fields.DateTime(dump_only=True)
    workout_exercises = fields.Nested(
        WorkoutExerciseSchema,
        many=True,
        dump_only=True
    )

    @validates_schema
    def validate_text(self, data, **kwargs):
        for field_name in ("name", "description"):
            value = data.get(field_name)
            if value is not None and not value.strip():
                raise ValidationError({
                    field_name: ["This field cannot be blank."]
                })
