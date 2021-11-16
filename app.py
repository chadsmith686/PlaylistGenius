import requests
from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db
from secret import USER_AGENT, API_SECRET_KEY

API_BASE_URL = "https://ws.audioscrobbler.com/2.0/"

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


def lastfm_get(payload):
    # define headers and URL
    headers = {'user-agent': USER_AGENT}
    url = 'https://ws.audioscrobbler.com/2.0/'

    # Add API key and format to the payload
    payload['api_key'] = API_SECRET_KEY
    payload['format'] = 'json'

    response = requests.get(url, headers=headers, params=payload)
    return response

@app.route('/go')
def get_similar_tracks():
    artist = request.args["artist"]
    track = request.args["track"]
    requests.get(f"{API_BASE_URL}/", params={'artist': artist, 'track': track})