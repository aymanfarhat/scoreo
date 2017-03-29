import time
from unittest import TestCase
import flask
from sqlalchemy.exc import IntegrityError 
from scoreo import models
from scoreo import create_test_app


class GameTest(TestCase):
    def setUp(self):
        self.db = models.db

        self.app = create_test_app()
        self.db.init_app(self.app)

        with self.app.app_context():
            self.db.create_all()

    def tearDown(self):
        with self.app.app_context():
            self.db.drop_all()

    def test_create(self):
        with self.app.app_context():
            game = models.Game.create('nunu')

            target_game = self.db.session.query(models.Game) \
                            .filter(models.Game.slug == 'nunu').first()

            self.assertEqual(game, target_game)

            with self.assertRaises(IntegrityError):
                models.Game.create('nunu')


    def test_first_or_create(self):
        with self.app.app_context():
            ngame = models.Game.first_or_create('nunu')
            game2 = models.Game.first_or_create('nunu')

            self.assertEqual(ngame, game2)

            ngame = models.Game.first_or_create('ayman')
            game2 = models.Game.first_or_create('freddy')

            self.assertNotEqual(ngame, game2)


class BoardTest(TestCase):
    def setUp(self):
        self.db = models.db

        self.app = create_test_app()
        self.db.init_app(self.app)

        with self.app.app_context():
            self.db.create_all()

    def tearDown(self):
        with self.app.app_context():
            self.db.drop_all()

    def test_first_or_create(self):
        with self.app.app_context():
            game = models.Game.first_or_create('nunu')
            board = models.Board.first_or_create('top10', game)

            game2 = models.Game.first_or_create('nunu')
            board2 = models.Board.first_or_create('top10', game2)

            self.assertEqual(game, game2)

            board3 = models.Board.first_or_create('top20', game)

            self.assertNotEqual(board2, board3)

class PlayerTest(TestCase):
    def setUp(self):
        self.db = models.db

        self.app = create_test_app()
        self.db.init_app(self.app)

        with self.app.app_context():
            self.db.create_all()

    def tearDown(self):
        with self.app.app_context():
            self.db.drop_all()

    def test_first_or_create(self):
        with self.app.app_context():
            player = models.Player.first_or_create('ayman', '1234')
            player1 = models.Player.first_or_create('ayman', '1234')

            self.assertEqual(player, player1)

            countplayer = self.db.session.query(models.Player) \
                        .filter(models.Player.fb_id == player.fb_id).count()

            self.assertEqual(1, countplayer)
