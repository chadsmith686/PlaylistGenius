import requests
import pdb
from flask import Flask, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Song, Playlist
from secret import API_KEY

API_BASE_URL = "https://ws.audioscrobbler.com/2.0/"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///playlist-genius'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "its a secret!"

connect_db(app)
db.create_all()

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

    data = r.json()  # convert json data into string
    json_tracks = data["similartracks"]["track"]

    return render_template("results.html", tracks=json_tracks, artist=artist, track=track)


# @app.route('/playlists/add')
# def add_to_playlist():
#     artist = request.args["artist"]
#     track = request.args["track"]
#     headers = {'User-Agent': 'chadsmithmusic@icloud.com'}
#     r = requests.get(f"{API_BASE_URL}?method=track.getsimilar&artist={artist}&track={track}&api_key={API_KEY}&format=json",
#                  params={'artist': artist, 'track': track}, headers=headers)

#     data = r.json()  # convert json data into string
#     json_tracks = data["similartracks"]["track"]

#     for track in json_tracks:
#         artist_name = track["artist"]["name"]
#         song_name = track["name"]
#         insert_song = Song(song_name=song_name, artist_name=artist_name)
#         db.session.add(insert_song)
#         db.session.commit()


@app.route('/playlists')
def show_playlists():
    database_response = Playlist.query.all()
    return render_template('playlists.html', playlists=database_response)


@app.route("/songs")
def show_songs():
    songs = Song.query.all()
    return render_template("songs.html", songs=songs)
