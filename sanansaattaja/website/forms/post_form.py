from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    topic = StringField('Тема')
    text = TextAreaField("Текст", validators=[DataRequired()])
    is_public = BooleanField('Видно всем', default=True)
    submit = SubmitField('Опубликовать')