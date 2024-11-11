'''initializes the Flask app'''
import os
from flask import Flask

import env # noqa - imports variables from env.py

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY')

from chorerate import routes # noqa - imports routes from routes.py
