from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, SubmitField, IntegerField, RadioField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    nickname = StringField('Nickname', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Password again', validators=[DataRequired()])
    name = StringField('First name', validators=[DataRequired()])
    surname = StringField('Second name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    sex = RadioField('Sex', choices=[('male', 'Male'), ('female', 'Female'), ('helicopter', 'Helicopter')])
    photo = FileField('Add image (jpg, png, gif); max file size = 1 MB')
    submit = SubmitField('Finish')
