import requests
from flask import Flask, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from models import connect_db
from secret import API_KEY 

API_BASE_URL = "https://ws.audioscrobbler.com/2.0/"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///playlist-genius'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "its a secret!"

db = SQLAlchemy(app)
connect_db(app)

debug = DebugToolbarExtension(app)

@app.route('/')
def root():
    """Displays home page."""
    return render_template('index.html')

@app.route('/search')
def get_similar_tracks():
    artist = request.args["artist"]
    track = request.args["track"]  
    headers = {'User-Agent': 'chadsmithmusic@icloud.com'}
    r = requests.get(f"{API_BASE_URL}?method=track.getsimilar&artist={artist}&track={track}&api_key={API_KEY}&format=json", 
                    params={'artist': artist, 'track': track}, headers=headers)

    data = r.json()
    tracks = data["similartracks"]["track"]

    return render_template("results.html", data=data, tracks=tracks, artist=artist, track=track)