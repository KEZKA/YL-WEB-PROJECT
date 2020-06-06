from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):
    text = TextAreaField("Text", validators=[DataRequired()])
    submit = SubmitField('Publish')
