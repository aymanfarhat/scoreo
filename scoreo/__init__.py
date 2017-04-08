import configparser
import flask
from flask_migrate import Migrate


def create_app(mode='dev'):
    config = configparser.ConfigParser()
    config.read('config.ini')
    section = config[mode]

    DATABASE_URI = 'mysql://{0}:{1}@{2}/{3}'.format(
            section['DB_USER'],
            section['DB_PASSWORD'],
            section['DB_HOST'],
            section['DB_NAME']
        )

    app = flask.Flask(__name__, static_url_path='/static')
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from scoreo import models

    models.db.init_app(app)

    if mode != 'test':
        migrate = Migrate(app, models.db)

    return app

app = create_app()
import scoreo.views, scoreo.commands  # noqa
