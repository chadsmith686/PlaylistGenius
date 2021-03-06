from secret import API_KEY
import requests, os
from flask import Flask, render_template, redirect, request, send_from_directory, jsonify
from models import db, connect_db, Song, Playlist
from flask_cors import CORS

from secret import API_KEY
app = Flask(__name__,  static_url_path='')
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///playlist-genius'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "hellosecret1"

# Heroku config:
# API_KEY = os.environ.get('API_KEY', '00000000')

# app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
#     'DATABASE_URL', "postgres:///playlistgenius").replace("://", "ql://", 1)
# app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY', 'hellosecret1')

API_BASE_URL = "https://ws.audioscrobbler.com/2.0/"

connect_db(app)
db.create_all()

@app.route('/')
def root():
    """Displays home page."""
    return render_template('index.html')

@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

@app.route('/search')
def get_similar_tracks():
    artist = request.args["artist"]
    track = request.args["track"]
    headers = {'User-Agent': 'chadsmithmusic@icloud.com'}
    r = requests.get(f"{API_BASE_URL}?method=track.getsimilar&artist={artist}&track={track}&api_key={API_KEY}&format=json",
                     params={'artist': artist, 'track': track}, headers=headers)

    data = r.json()  # convert json data into string
    json_tracks = data["similartracks"]["track"]

    return render_template("results.html", tracks=json_tracks, artist=artist, track=track)

@app.route('/new')
def create_new_playlist():
    '''Shows a form that allows user to create new playlist'''

    return render_template('new.html')

@app.route('/created')
def show_created_playlist():

    return render_template('created.html')

@app.route('/new/<int:_id>', methods=["POST"])
def make_new_playlist(_id):
    name = request.form["name"]
    description = request.form["description"]
    insert_playlist = Playlist(id=_id, name=name, description=description)
    db.session.add(insert_playlist)
    db.session.commit()
    return render_template('created.html', id=_id, name=name, description=description)

@app.route('/playlists', methods=["POST"])
def show_playlists():
    database_response = Playlist.query.all()
    return render_template('playlists.html', playlists=database_response)

@app.route("/songs")
def show_songs():
    songs = Song.query.all()
    return render_template("songs.html", songs=songs)

if __name__ == "__main__": 
    app.run(debug=True)