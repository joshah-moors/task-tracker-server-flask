#! /usr/bin/env python3
'''
Back-end server for a task tracker web app.
Following this guide:
    https://testdriven.io/blog/developing-a-single-page-app-with-flask-and-vuejs/
'''

import os
import pickle
import uuid

from flask import Flask, jsonify, request
from flask_cors import CORS

# configuration
DEBUG = True
PICKLE_FILE = 'app_data.pickle'

# instantiate app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={f'/*': {'origins': '*'}})

# supporting functions
def load_app_data():
    with open(PICKLE_FILE, 'rb') as f:
        return pickle.load(f)

def save_app_data():
    with open(PICKLE_FILE, 'wb') as f:
        pickle.dump(TASKS, f)

def remove_task(task_id):
    try:
        TASKS.remove(next((item for item in TASKS if item['id'] == task_id), None))
        save_app_data()
        return True
    except ValueError:
        return False

# initialize the data (small pickle data for testing)
if os.path.exists(PICKLE_FILE):
    TASKS = load_app_data()
else:
    TASKS = [
        {
            'id': uuid.uuid4().hex,
            'title': 'Scaffold front-end',
            'owner': 'Joshah',
            'complete': False
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
            'complete': True
        },
    ]
    save_app_data()

# test route
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
        save_app_data()
        response_object['message'] = 'Task added!'
    else:
        response_object['tasks'] = TASKS
    return jsonify(response_object)

@app.route('/tasks/<task_id>', methods=['PUT', 'DELETE'])
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
        save_app_data()
        response_object['message'] = 'Task updated!'
    elif request.method == 'DELETE':
        remove_task(task_id)
        response_object['message'] = 'Task removed!'
    return jsonify(response_object)


if __name__ == '__main__':
    app.run()