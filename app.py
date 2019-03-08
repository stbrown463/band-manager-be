from flask import Flask, g, render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash
from flask_cors import CORS

from resources.bands import bands_api
from resources.genres import genres_api
from resources.venues import venues_api
from resources.contacts import contacts_api

import models
import os

DEBUG = True
PORT = 8000

app = Flask(__name__)


CORS(bands_api, origins=["Heroku FE link here", "http://localhost:3000"], supports_credentials=True)
CORS(genres_api, origins=["Heroku FE link here", "http://localhost:3000"], supports_credentials=True)
CORS(venues_api, origins=["Heroku FE link here", "http://localhost:3000"], supports_credentials=True)
CORS(contacts_api, origins=["Heroku FE link here", "http://localhost:3000"], supports_credentials=True)

app.register_blueprint(bands_api, url_prefix='/api/v1')
app.register_blueprint(genres_api, url_prefix='/api/v1')
app.register_blueprint(venues_api, url_prefix='/api/v1')
app.register_blueprint(contacts_api, url_prefix='/api/v1')

@app.route('/')
def hello_world():
    return 'Hello World'



if 'HEROKU' in os.environ:
    print('hitting ')
    models.initialize()
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)