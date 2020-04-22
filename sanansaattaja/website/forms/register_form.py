from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, IntegerField, RadioField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    age = IntegerField('Возраст', validators=[DataRequired()])
    sex = RadioField('Ваш пол', choices=[('male', 'Мужской'), ('female', 'Женский')])
    photo = FileField('Выберите фото (jpg, png, gif)', validators=[FileAllowed(['jpg', 'png'], 'Только картинки!')])
    submit = SubmitField('Зарегистрироваться')
