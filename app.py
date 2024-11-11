'''Main app file for the Flask app'''
import os
from flask import Flask, render_template
import env # noqa - imports variables from env.py

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY')


@app.route('/')
def homepage():
    '''View for the homepage'''
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host=os.environ.get('IP', '0.0.0.0'),
            port=int(os.environ.get('PORT', 5000)),
            debug=os.environ.get('DEBUG', False))
