#! /usr/bin/env python3
'''
Back-end server for a task tracker web app.
Following this guide:
    https://testdriven.io/blog/developing-a-single-page-app-with-flask-and-vuejs/
'''

import uuid

from flask import Flask, jsonify, request
from flask_cors import CORS

# configuration
DEBUG = True

TASKS = [
    {
        'id': uuid.uuid4().hex,
        'title': 'Scaffold front-end',
        'owner': 'Joshah',
        'complete': True
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Production JS Server',
        'owner': 'N/A',
        'complete': False
    },
    {
        'id': uuid.uuid4().hex,
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

# supporting functions
def remove_task(task_id):
    for task in TASKS:
        if task['id'] == task_id:
            TASKS.remove(task)
            return True
    return False

# first route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/tasks', methods=['GET', 'POST'])
def all_tasks():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        TASKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'owner': post_data.get('owner'),
            'complete': post_data.get('complete')
        })
        response_object['message'] = 'Task added!'
    else:
        response_object['tasks'] = TASKS
    return jsonify(response_object)

@app.route('/tasks/<task_id>', methods=['PUT'])
def single_task(task_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_task(task_id)
        TASKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'owner': post_data.get('owner'),
            'complete': post_data.get('complete')
            })
        response_object['message'] = 'Task updated!'
    return jsonify(response_object)


if __name__ == '__main__':
    app.run()