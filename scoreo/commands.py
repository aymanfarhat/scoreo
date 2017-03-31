from scoreo import app
from scoreo import models


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database tables"""
    models.db.create_all()
    print('Initialized the database.')

@app.cli.command('initgame')
def initgame_command():
    """Initializes a new game with secret
    or gets a matching one if same slug"""

    slug = input('Select game slug: ') 
    game = models.Game.first_or_create(slug)
    print('Your game secret is: ' + game.secret)
