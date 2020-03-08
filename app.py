#! /usr/bin/env python3
'''
Back-end server for a task tracker web app.
Following this guide:
    https://testdriven.io/blog/developing-a-single-page-app-with-flask-and-vuejs/
'''

from flask import Flask, jsonify
from flask_cors import CORS

# configuration
DEBUG = True

TASKS = [
    {
        'title': 'Scaffold front-end',
        'owner': 'Joshah',
        'complete': True
    },
    {
        'title': 'Production JS Server',
        'owner': 'N/A',
        'complete': False
    },
    {
        'title': 'Add CORS to Flask server',
        'owner': 'Joshah',
        'complete': False
    },
]

# instantiate app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={f'/*': {'origins': '*'}})

# first route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/tasks', methods=['GET'])
def all_tasks():
    return jsonify({
            'status': 'success',
            'tasks': TASKS
        })


if __name__ == '__main__':
    app.run()