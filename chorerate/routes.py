'''Contains the routes for the application'''
from flask import render_template
from chorerate import app


@app.route('/')
def homepage():
    '''View for the homepage'''
    return render_template('index.html')
