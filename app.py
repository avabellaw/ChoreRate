'''Main app file for the Flask app'''
import os
from flask import Flask
import env

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY')


@app.route('/')
def homepage():
    '''View for the homepage'''
    return '<h1>Homepage</h1>'


if __name__ == '__main__':
    app.run(host=os.environ.get('IP', '0.0.0.0'),
            port=int(os.environ.get('PORT', 5000)),
            debug=os.environ.get('DEBUG', False))
