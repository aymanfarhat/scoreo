import os
import uuid
import flask
from flask_migrate import Migrate


def create_app():
    DATABASE_URI = 'mysql://root:@localhost/scorio'

    app = flask.Flask(__name__, static_url_path='/static')
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from scoreo import models

    models.db.init_app(app)
    migrate = Migrate(app, models.db)


    return app

def create_test_app():
    DATABASE_URI = 'mysql://root:@localhost/scorio_test'

    app = flask.Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from scoreo import models

    models.db.init_app(app)


    return app


app = create_app()
import scoreo.views, scoreo.commands # noqa
