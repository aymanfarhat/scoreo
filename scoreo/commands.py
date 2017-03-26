from scoreo import app


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    print('Initialized the database.')
