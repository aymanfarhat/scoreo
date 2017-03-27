from scoreo import app
from scoreo import db
from scoreo import models


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database tables"""
    db.create_all()
    print('Initialized the database.')
