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

            self.assertEqual(game, (target_game.slug, target_game.secret))

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
