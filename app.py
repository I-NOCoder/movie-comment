# -*- coding:utf-8 -*-
from collections import OrderedDict
from flask import Flask
from werkzeug.wsgi import DispatcherMiddleware

import config
from views import backend, json_api
from ext import db


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config)
    db.init_app(app)
    app.register_blueprint(backend.bd)
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, OrderedDict((
        ('/j', json_api),
    )))

    return app

app = create_app()


if __name__ == "__main__":

    app.run(host='0.0.0.0', port=8100, debug=app.debug)
