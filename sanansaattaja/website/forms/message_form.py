from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class MessageForm(FlaskForm):
    addressee = StringField('Кому', validators=[DataRequired()])
    text = TextAreaField("Текст", validators=[DataRequired()])
    submit = SubmitField('Отправить')