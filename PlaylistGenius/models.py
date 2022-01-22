from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref, relationship

db = SQLAlchemy()

class Playlist(db.Model):

    __tablename__ = 'playlist'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    songs = db.relationship('Song', secondary='playlists_songs', backref='playlist')

class Song(db.Model):

    __tablename__ = 'song'

    id = db.Column(db.Integer, primary_key=True)
    song_name = db.Column(db.String, nullable=False)
    artist_name = db.Column(db.String, nullable=False)

class PlaylistSong(db.Model):
    """Mapping of a playlist to a song."""

    __tablename__ = "playlists_songs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    song_id = db.Column(db.Integer, db.ForeignKey("song.id"))
    playlist_id = db.Column(db.Integer, db.ForeignKey("playlist.id"))

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)