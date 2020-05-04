from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired


class PasswordChangeForm(FlaskForm):
    old_password = PasswordField(' Old password', validators=[DataRequired()])
    password = PasswordField('New password', validators=[DataRequired()])
    password_again = PasswordField('New password again', validators=[DataRequired()])
    submit = SubmitField('Change Password')
