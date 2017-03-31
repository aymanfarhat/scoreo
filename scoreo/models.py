import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    fb_id = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, name, fb_id):
        self.fb_id = fb_id
        self.name = name

    def __repr__(self):
        return '<Player %r>' % self.name

    @classmethod
    def first_or_create(cls, name, fb_id):
        player = cls.query.filter(cls.fb_id == fb_id).first()

        if player is not None:
            result = player
        else:
            result = cls(name, fb_id)
            db.session.add(result)
            db.session.commit()

        return result 

    @classmethod
    def find_by_fbid(cls, fb_id):
        return cls.query.filter(cls.fb_id == fb_id).first()


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

    @classmethod
    def insert(cls, value, player, board):
        score = cls(value, player, board)
        return score


class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    game = db.relationship('Game',
                    backref=db.backref('boards', lazy='dynamic'))

    def __init__(self, slug, game):
        self.slug = slug
        self.game_id = game.id
        self.game = game

    def __repr__(self):
        return '<Board %r>' % self.slug

    @classmethod
    def create(cls, slug, game):
        board = cls(slug, game)

        db.session.add(board)
        db.session.commit()

        return board

    @classmethod
    def first_or_create(cls, slug, game):
        board = cls.query.filter(cls.slug == slug and cls.game == game).first()

        if board is not None:
            result = board
        else:
            result = cls.create(slug, game)

        return result 

    @classmethod
    def find_by_slug(cls):
        pass

    @classmethod
    def get_board_scores_by_player(cls, player_id, limit=10, sort_by='date', sort_order='DESC'):
        """List of scores history by a user on a board
        returns a list of scores with datetime for each entry
        """
        pass

    @classmethod
    def get_board_topn_scores(cls, slug, limit=10, sort_order='DESC'):
        """Returns top n scores by a board id"""
    pass


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(80), unique=True, nullable=False)
    secret = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, slug):
        self.slug = slug
        self.secret = str(uuid.uuid1())

    def __repr__(self):
        return '<Game %r>' % self.slug

    @classmethod
    def create(cls, slug):
        game = cls(slug)

        db.session.add(game)
        db.session.commit()

        return game

    @classmethod
    def first_or_create(cls, slug):
        game = cls.query.filter_by(slug = slug).first()

        if game is not None:
            result = game
        else:
            result = cls.create(slug)

        return result 
