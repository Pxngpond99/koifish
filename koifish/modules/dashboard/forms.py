from flask_wtf import FlaskForm
from wtforms import fields


class SelectTimeRange(FlaskForm):
    time = fields.SelectField(
        "ช่วงเวลา (วินาที)",
        choices=[
            (10, "10 วินาที"),
            (30, "30 วินาที"),
            (60, "60 วินาที"),
        ],
        default=60,
    )
    bin = fields.SelectField(
        "Bins Heatmap",
        choices=[
            (10, "10"),
            (20, "20"),
            (50, "50"),
        ],
        default=20,
    )
