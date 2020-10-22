from application import app
from flask import request,jsonify

import json

@app.route('/')
def test():
    return 'Application is running'
