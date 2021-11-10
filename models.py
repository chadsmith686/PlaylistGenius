from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref, relationship

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
