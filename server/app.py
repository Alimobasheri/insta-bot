from flask import Flask, request, send_file, render_template, url_for

import json
import requests
import os

from . import db

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    app.config.from_object('server.config.Config')

    db.init_app(app)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    '''
    @app.route('/', defaults={'past_days': None})
    @app.route('/<past_days>')
    def bing_background_url(past_days=None):

        data_json = {'result': []}
        if past_days != None:
            data = bing.bing_background(0, int(past_days)-1)
            # for i in data:
            # details = {}
            # details['url'] = i
            # data_json['result'].append(details)
            return render_template("index.html", data_list=data)
        else:
            data_list = []
            data_list.append(bing.bing_background_for_given_day(0))
            return render_template("index.html", data_list=data_list)

    @app.route('/Today-image')
    def today_img():
        res = bing.bing_background_for_given_day(0)
        data_json = json.dumps(res)

        return (data_json)
    '''
    with app.app_context():
        from . import routes
        db.create_all()
        return app