from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, IntegerField, RadioField
from wtforms.validators import DataRequired


class EditProfileForm(FlaskForm):
    nickname = StringField('Nickname', validators=[DataRequired()])
    name = StringField('First name', validators=[DataRequired()])
    surname = StringField('Second name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    sex = RadioField('Sex', choices=[('male', 'Male'), ('female', 'Female'), ('helicopter', 'Helicopter')])
    photo = FileField('Add image (jpg, png, gif); max file size = 1 MB')
    submit = SubmitField('Save changes')
    check_deletion = StringField('stay')
