from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    topic = StringField('Topic')
    text = TextAreaField("Text", validators=[DataRequired()])
    is_public = BooleanField('Everyone can see', default=True)
    submit = SubmitField('Publish')
