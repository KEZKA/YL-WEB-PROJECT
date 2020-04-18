from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    topic = StringField('Тема')
    text = TextAreaField("Текст", validators=[DataRequired()])
    remember_me = BooleanField('Видно всем')
    submit = SubmitField('Опубликовать')