'''Main app file for the Flask app'''
import os
from chorerate import app

if __name__ == '__main__':
    app.run(host=os.environ.get('IP', '0.0.0.0'),
            port=int(os.environ.get('PORT', 5000)),
            debug=eval(os.environ.get('DEBUG', False)))
