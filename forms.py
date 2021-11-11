from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired

class SearchForm(FlaskForm):
    """Form for adding snacks."""

    title = StringField("Song Title", validators=[InputRequired()])
    artist = StringField("Artist Name", validators=[InputRequired()])
