import flask
from scoreo import app
from scoreo.models import Game, Player, Score, Board


def compose_reply(status='success', data=''):
    return {
        'status': status,
        'data': data
    }

@app.route('/')
def index():
    return 'It runs!'

@app.route('/score/add', methods=['POST'])
def add_score():
    """Add a new score, user should supply:
    - game_slug
    - board_slug
    - fb_id
    - fb_access_token
    - score_value
    """

    # Check if game and board exists

    data = flask.request.form

    # before all this needs to validate that all data was actually sent

    game = Game.find_by_slug(data['game_slug'])

    reply = {}

    if game is not None:
        board = Board.first_or_create(data['board_slug'], game)

        try:
            player = Player.create_by_access_token(data['fb_access_token'])
        except ValueError as error:
            return flask.jsonify(compose_reply('error', str(error)))

        score = Score.insert(int(data['score_value']), player, board)

        reply = compose_reply('success', {
            'score': score.value,
            'board': board.slug,
            'game': game.slug, 
            'player': {'name': player.name, 'fb_id': player.fb_id, 'fb_access_token': player.fb_access_token},
            'created_at': score.created_at
        })
    else:
        reply = compose_reply('error', 'Game does not exist')


    return flask.jsonify(reply)


@app.route('/leaderboard/<game_slug>/<board_slug>')
def get_board(game_slug, board_slug):
    game = Game.find_by_slug(game_slug)

    reply = {}

    if game is not None:
        board = Board.first_or_create(board_slug, game)

        board_data = board.get_topn_scores()

        reply = compose_reply('success', board_data)
    else:
        reply = compose_reply('error', 'Game does not exist')

    return flask.jsonify(reply)


@app.route('/playerboard/<game_slug>/<board_slug>/<fb_id>')
def playerboard(game_slug, board_slug, fb_id):
    player = Player.find_by_fbid(fb_id)

    game = Game.find_by_slug(game_slug)

    reply = {}

    if game is not None:
        board = Board.first_or_create(board_slug, game)

        if player is not None:
            board_data = board.get_board_scores_by_player(player.id)

            reply = compose_reply('success', board_data)
        else:
            reply = compose_reply('error', 'Player does not exist')

    else:
        reply = compose_reply('error', 'Game does not exist')

    return flask.jsonify(reply)
