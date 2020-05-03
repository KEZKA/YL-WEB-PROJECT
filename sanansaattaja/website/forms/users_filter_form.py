from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, RadioField


class FilterForm(FlaskForm):
    email = StringField('Email')
    name = StringField('First name')
    surname = StringField('Second name')
    age = IntegerField('More than')
    sex = RadioField('Sex', choices=[('male', 'Male'),
                                      ('female', 'Female'), ('helicopter', 'Helicopter'), ('all', 'All')])
    submit = SubmitField('Find')
