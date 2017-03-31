import uuid
from datetime import datetime
import requests
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, desc
from sqlalchemy import func


db = SQLAlchemy()

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    fb_id = db.Column(db.String(80), unique=True, nullable=False)
    fb_access_token = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, name, fb_id, token):
        self.fb_id = fb_id
        self.name = name
        self.fb_access_token = token

    def __repr__(self):
        return '<Player %r>' % self.name

    @classmethod
    def first_or_create(cls, name, fb_id, token):
        player = cls.query.filter(cls.fb_id == fb_id).first()

        if player is not None:
            result = player
        else:
            result = cls(name, fb_id, token)
            db.session.add(result)
            db.session.commit()

        return result 

    @classmethod
    def find_by_fbid(cls, fb_id):
        return cls.query.filter(cls.fb_id == fb_id).first()

    @classmethod
    def create_by_access_token(cls, access_token):
        playload = {
            'access_token': access_token,
            'fields': 'id,name' 
        }

        r = requests.get('https://graph.facebook.com/me', params=playload)

        reply_data = r.json()

        player = cls.first_or_create(reply_data['name'], reply_data['id'], access_token)

        return player


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

    def __init__(self, value, player, board, created_at='now'):
        self.value = value
        self.player = player
        self.board = board

        if created_at != 'now':
            self.created_at = created_at

    def __repr__(self):
        return '<Score %r>' % self.value

    @classmethod
    def insert(cls, value, player, board, created_at='now'):
        score = cls(value, player, board, created_at)

        db.session.add(score)
        db.session.commit()

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

    def get_board_scores_by_player(self, player_id, limit=10, sort_by=Score.value, sort_order='DESC'):
        """List of scores history by a user on a board
        returns a list of scores with datetime for each entry
        """

        sort_funcs = {
            'DESC': desc,
            'ASC': asc
        }

        board_scores = db.session.query(Score.value, Score.created_at) \
                        .filter_by(player_id=player_id) \
                        .filter_by(board_id=self.id) \
                        .order_by(sort_funcs[sort_order](sort_by)) \
                        .limit(limit) \
                        .all()

        return [{'score': r[0], 'created_at': r[1]} for r in board_scores]


    def get_topn_scores(self, limit=10, sort_order='DESC'):
        """Returns top n scores by a board id"""

        sort_funcs = {
            'DESC': desc,
            'ASC': asc
        }

        board_scores = db.session.query(func.max(Score.value), Score.created_at, Player.name, Player.fb_id) \
                        .filter_by(board_id=self.id) \
                        .join(Player) \
                        .order_by(sort_funcs[sort_order](Score.value)) \
                        .distinct(Player.id) \
                        .group_by(Player.name) \
                        .limit(limit) \
                        .all()

        return [{'score': r[0], 'created_at': r[1], 'player_name': r[2], 'player_fbid': r[3]} for r in board_scores]


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

    def get_board_by_slug(self, board_slug):
        return self.boards.filter_by(slug=board_slug).first()

    @classmethod
    def find_by_slug(cls, slug):
        return cls.query.filter(cls.slug == slug).first()
