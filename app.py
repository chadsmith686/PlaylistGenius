from flask import Flask, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db
from forms import SearchForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///playlist-genius'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "its a secret!"

connect_db(app)
# db.create_all()

debug = DebugToolbarExtension(app)

@app.route('/')
def root():
    """Displays home page."""
    return render_template('index.html')

