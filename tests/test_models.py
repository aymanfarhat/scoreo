import time
from unittest import TestCase
import flask
from sqlalchemy.exc import IntegrityError 
from sqlalchemy import and_
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

    def test_find_by_slug(self):
        pass

    def test_get_user_scores_by_board((self):
        """Validate the listing of scores in a board by a player"""
            game = models.Game.first_or_create('nunu')
            mode1_board = models.Board.first_or_create('mode1', game)
            player = models.Player.first_or_create('Ayman', '2334')

            models.Score.insert(360, player, mode1_board)
            models.Score.insert(380, player, mode1_board)
            models.Score.insert(400, player, mode1_board)
            models.Score.insert(600, player, mode1_board)
            models.Score.insert(23, player, mode1_board)
            models.Score.insert(5000, player, mode1_board)    

            #score_list = models.
        pass

    def test_get_board_topn_scores(self):
        """Validate the listing of top n players in a board"""
        pass


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

    def test_find_by_fbid(self):
        with self.app.app_context():
            player = models.Player.find_by_fbid('9999')

            self.assertIsNone(player)

            player = models.Player.first_or_create('Ayman', '9999')

            self.assertIsNotNone(player)
            self.assertEqual('9999', player.fb_id)


class ScoreTest(TestCase):
    def setUp(self):
        self.db = models.db

        self.app = create_test_app()
        self.db.init_app(self.app)

        with self.app.app_context():
            self.db.create_all()

    def tearDown(self):
        with self.app.app_context():
            self.db.drop_all()

    def test_log_player_scores(self):
        """Validate the logging of scores and their relations"""
        with self.app.app_context():
            # Setup a new game with a board and a player
            game = models.Game.first_or_create('nunu')
            board = models.Board.first_or_create('top10', game)
            board2 = models.Board.first_or_create('top30', game)
            player = models.Player.first_or_create('Ayman', '2334')
            player2 = models.Player.first_or_create('Armando', '1337')

            self.assertNotEqual(player, player2)

            # Log scores for player
            models.Score.insert(36, player, board)
            models.Score.insert(29, player, board)
            models.Score.insert(45, player, board)
            models.Score.insert(4000, player2, board)
            models.Score.insert(100, player, board2)
            models.Score.insert(5000, player, board2)

            all_player_scores = self.db.session.query(models.Score.value) \
                                    .filter_by(player_id=player.id) \
                                    .all()

            self.assertEqual([(36,), (29,), (45,), (100,), (5000,)], all_player_scores)

            board_scores = self.db.session.query(models.Score.value) \
                            .filter_by(player_id=player.id) \
                            .filter_by(board_id=board.id) \
                            .all()

            self.assertEqual([(36,), (29,), (45,)], board_scores)
