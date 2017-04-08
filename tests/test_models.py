import time
import uuid
from datetime import datetime
from unittest import TestCase
import flask
from sqlalchemy.exc import IntegrityError 
from sqlalchemy import and_
from scoreo import models
from scoreo import create_app


class GameTest(TestCase):
    def setUp(self):
        self.db = models.db

        self.app = create_app('test')
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


    def test_get_board_by_slug(self):
        with self.app.app_context():
            game = models.Game.first_or_create('nana') 

            self.assertIsNone(game.get_board_by_slug('b1'))

            board = models.Board.first_or_create('b1', game)

            board_query = game.get_board_by_slug('b1')

            self.assertIsNotNone(board_query)
            self.assertEqual('b1', board_query.slug)


class BoardTest(TestCase):
    def setUp(self):
        self.db = models.db

        self.app = create_app('test')
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



    def test_get_board_scores_by_player(self):
        with self.app.app_context():
            """Validate the listing of scores in a board by a player"""
            game = models.Game.first_or_create('nunu')
            mode1_board = models.Board.first_or_create('mode1', game)
            player = models.Player.first_or_create('Ayman', '2334', uuid.uuid1())

            dummy_datetime = datetime(2017, 3, 31, 8, 59, 2, 0)

            models.Score.insert(360, player, mode1_board, dummy_datetime)
            models.Score.insert(380, player, mode1_board, dummy_datetime)
            models.Score.insert(400, player, mode1_board, dummy_datetime)
            models.Score.insert(600, player, mode1_board, dummy_datetime)
            models.Score.insert(23, player, mode1_board, dummy_datetime)
            models.Score.insert(5000, player, mode1_board, dummy_datetime)
            models.Score.insert(1, player, mode1_board, dummy_datetime)
            models.Score.insert(2, player, mode1_board, dummy_datetime)
            models.Score.insert(3, player, mode1_board, dummy_datetime)
            models.Score.insert(4, player, mode1_board, dummy_datetime)
            models.Score.insert(5, player, mode1_board, dummy_datetime)

            score_list = mode1_board.get_board_scores_by_player(player.id)

            expected_score_list = [
                    { 'score': 5000, 'created_at': dummy_datetime},
                    { 'score': 600, 'created_at': dummy_datetime},
                    { 'score': 400, 'created_at': dummy_datetime},
                    { 'score': 380, 'created_at': dummy_datetime},
                    { 'score': 360, 'created_at': dummy_datetime},
                    { 'score': 23, 'created_at': dummy_datetime},
                    { 'score': 5, 'created_at': dummy_datetime},
                    { 'score': 4, 'created_at': dummy_datetime},
                    { 'score': 3, 'created_at': dummy_datetime},
                    { 'score': 2, 'created_at': dummy_datetime},
            ] 

            self.assertEqual(len(expected_score_list), len(score_list))

            self.assertEqual(expected_score_list, score_list)


    def test_get_board_topn_scores(self):
        """Validate the listing of top n players in a board"""

        with self.app.app_context():
            game = models.Game.first_or_create('nunu')
            mode1_board = models.Board.first_or_create('mode1', game)
            mode2_board = models.Board.first_or_create('mode2', game)

            player1 = models.Player.first_or_create('Ayman', '2334', uuid.uuid1())
            player2 = models.Player.first_or_create('Tony', '2335', uuid.uuid1())
            player3 = models.Player.first_or_create('Armando', '2336', uuid.uuid1())

            dummy_datetime = datetime(2017, 3, 31, 8, 59, 2, 0)

            models.Score.insert(360, player3, mode1_board, dummy_datetime)
            models.Score.insert(380, player3, mode1_board, dummy_datetime)
            models.Score.insert(400, player2, mode1_board, dummy_datetime)
            models.Score.insert(600, player2, mode1_board, dummy_datetime)
            models.Score.insert(23, player2, mode1_board, dummy_datetime)
            models.Score.insert(5000, player1, mode1_board, dummy_datetime)
            models.Score.insert(1, player1, mode1_board, dummy_datetime)
            models.Score.insert(2, player1, mode1_board, dummy_datetime)
            models.Score.insert(3, player1, mode1_board, dummy_datetime)
            models.Score.insert(4, player2, mode1_board, dummy_datetime)
            models.Score.insert(5, player1, mode1_board, dummy_datetime)
            models.Score.insert(5, player1, mode2_board, dummy_datetime)
            models.Score.insert(5, player1, mode2_board, dummy_datetime)
            models.Score.insert(5, player1, mode2_board, dummy_datetime)
            models.Score.insert(5, player1, mode2_board, dummy_datetime)

            expected_score_list = [
                    { 'score': 5000, 'created_at': dummy_datetime, 'player_fbid': '2334', 'player_name': 'Ayman'},
                    { 'score': 600, 'created_at': dummy_datetime, 'player_fbid': '2335', 'player_name': 'Tony'},
                    { 'score': 380, 'created_at': dummy_datetime, 'player_fbid': '2336', 'player_name': 'Armando'},
            ] 

            top4 = mode1_board.get_topn_scores(10)

            self.assertEqual(expected_score_list, top4)

            topn = mode2_board.get_topn_scores(4)

            self.assertEqual(1, len(topn))


class PlayerTest(TestCase):
    def setUp(self):
        self.db = models.db

        self.app = create_app('test')
        self.db.init_app(self.app)

        with self.app.app_context():
            self.db.create_all()

    def tearDown(self):
        with self.app.app_context():
            self.db.drop_all()

    def test_first_or_create(self):
        with self.app.app_context():
            player = models.Player.first_or_create('ayman', '1234', uuid.uuid1())
            player1 = models.Player.first_or_create('ayman', '1234', uuid.uuid1())

            self.assertEqual(player, player1)

            countplayer = self.db.session.query(models.Player) \
                        .filter(models.Player.fb_id == player.fb_id).count()

            self.assertEqual(1, countplayer)

    def test_find_by_fbid(self):
        with self.app.app_context():
            player = models.Player.find_by_fbid('9999')

            self.assertIsNone(player)

            player = models.Player.first_or_create('Ayman', '9999', uuid.uuid1())

            self.assertIsNotNone(player)
            self.assertEqual('9999', player.fb_id)


class ScoreTest(TestCase):
    def setUp(self):
        self.db = models.db

        self.app = create_app('test')
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
            player = models.Player.first_or_create('Ayman', '2334', uuid.uuid1())
            player2 = models.Player.first_or_create('Armando', '1337', uuid.uuid1())

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
