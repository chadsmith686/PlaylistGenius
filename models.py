from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref, relationship

db = SQLAlchemy()

class Song(db.Model):

    __tablename__ = '__songs__'

    id = db.Column(db.Integer, primary_key=True)
    song_name = db.Column(db.String, nullable=False)

class Artist(db.Model):

    __tablename__ = '__artists__'

    id = db.Column(db.Integer, primary_key=True)
    artist_name = db.Column(db.String, nullable=False)

class SongArtist(db.Model):

    __tablename__ = '__songs_artists__'

    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey("songs.id"))
    artist_id = db.Column(db.Integer, db.ForeignKey("playlists.id"))

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)