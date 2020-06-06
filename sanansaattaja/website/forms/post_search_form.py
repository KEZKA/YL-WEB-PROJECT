from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class PostSearchForm(FlaskForm):
    text = StringField("Search")
    submit = SubmitField('Search')
