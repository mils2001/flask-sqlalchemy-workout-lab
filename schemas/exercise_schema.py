
from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100)
    )
    category = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=50)
    )
    description = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=255)
    )
    created_at = fields.DateTime(dump_only=True)

    @validates_schema
    def validate_text(self, data, **kwargs):
        for field_name in ("name", "category", "description"):
            value = data.get(field_name)
            if value is not None and not value.strip():
                raise ValidationError({
                    field_name: ["This field cannot be blank."]
                })
