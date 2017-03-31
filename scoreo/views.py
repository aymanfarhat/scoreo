import flask
from scoreo import app
from scoreo.models import Game, Player, Score, Board


def compose_reply(status='success', data=''):
    return {
        'status': status,
        'data': data
    }

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

        player = Player.find_by_fbid(data['fb_id'])

        if player is None:
            player = Player.create_by_access_token(data['fb_access_token'])
        
        score = Score.insert(int(data['score_value']), player, board)

        reply = flask.jsonify('success', {
            'score': score.value,
            'board': board.slug,
            'game': game.slug, 
            'player': {'name': player.name, 'fb_id': player.fb_id},
            'created_at': score.create_at
            })
    else:
        reply = compose_reply('error', 'Game does not exist')

    return flask.jsonify(reply)
