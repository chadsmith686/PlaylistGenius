import requests, os
from flask import Flask, render_template, request, send_from_directory, jsonify
from models import db, connect_db, Song, Playlist
from secret import API_KEY

API_BASE_URL = "https://ws.audioscrobbler.com/2.0/"
API_KEY = os.environ.get('API_KEY', '00000000')

app = Flask(__name__,  static_url_path='')
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    'DATABASE_URL', "postgres:///playlistgenius").replace("://", "ql://", 1)
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY', 'hellosecret1')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

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

@app.route('/playlists/add', methods=['POST']) 
def add_to_playlist():  
    artist = request.json["artist"]
    track = request.json["track"]
    insert_song = Song(song_name=track, artist_name=artist)
    db.session.add(insert_song)
    db.session.commit()
    return jsonify(status='success')

@app.route('/playlists')
def show_playlists():
    database_response = Playlist.query.all()
    return render_template('playlists.html', playlists=database_response)

@app.route("/songs")
def show_songs():
    songs = Song.query.all()
    return render_template("songs.html", songs=songs)

if __name__ == "__main__": 
    app.run(debug=True)