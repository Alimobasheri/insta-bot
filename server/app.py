from flask import Flask, request, send_file, render_template, url_for

import json
import requests
import os

from . import db

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    app.config.from_object('server.config.Config')

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    with app.app_context():
        from . import routes
        db.create_all()
        return app