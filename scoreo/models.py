import uuid
from datetime import datetime
from scoreo import db


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    fb_id = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, fb_id, name):
        self.fb_id = fb_id
        self.name = name

    def __repr__(self):
        return '<Player %r>' % self.name


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    player = db.relationship('Player',
                    backref=db.backref('scores', lazy='dynamic'))

    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))
    board = db.relationship('Board',
                    backref=db.backref('scores', lazy='dynamic'))

    def __init__(self, value, player, board):
        self.value = value
        self.player = player
        self.board = board

    def __repr__(self):
        return '<Score %r>' % self.value


class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    game = db.relationship('Game',
                    backref=db.backref('boards', lazy='dynamic'))

    def __init__(self, slug, game):
        self.slug = slug
        self.game = game

    def __repr__(self):
        return '<Board %r>' % self.slug


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(80), unique=True, nullable=False)
    secret = db.Column(db.String(80), unique=True, default=str(uuid.uuid1()), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, slug):
        self.slug = slug

    def __repr__(self):
        return '<Game %r>' % self.slug
