import time
import flask
from unittest import TestCase
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

    def test_creation(self):
        game = models.Game('nba')

        with self.app.app_context():
            self.db.session.add(game)
            self.db.session.commit()

            target_game = self.db.session.query(models.Game).filter(models.Game.slug == 'nba').first()

            assert game == target_game
