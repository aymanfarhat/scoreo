import uuid
from datetime import datetime
from scoreo import db


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fb_id = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, fb_id, email):
        self.fb_id = fb_id
        self.email = email

    def __repr__(self):
        return '<Player %r>' % self.slug


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return '<Score %r>' % self.value


class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(80), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, slug):
        self.slug = slug

    def __repr__(self):
        return '<Board %r>' % self.slug


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(80), unique=True)
    secret = db.Column(db.String(80), unique=True, default=str(uuid.uuid1()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, slug):
        self.slug = slug

    def __repr__(self):
        return '<Game %r>' % self.slug
