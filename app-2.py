#!/usr/bin/env python

import os
import re
from flask import Flask
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request


app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': True
    }
]

# curl -i http://localhost:5000/todo/api/v1.0/tasks
@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})


# curl -i http://localhost:5000/todo/api/v1.0/tasks/2
# curl -i http://192.168.2.10:5000/todo/api/v1.0/tasks/2
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):

    # 获取计算机MAC地址和IP地址
    cmd = "ifconfig"
    result = exec_cmd(cmd)
    pat1 = r"ether ([\w:]+)"
    pat2 = r"inet ([\.\d]+)"
    MAC = re.findall(pat1, result)[0]       # 找到MAC
    IP = re.findall(pat2, result)[0]        # 找到IP
    print("MAC=%s, IP=%s" % (MAC, IP))
    tasks[1]['Mac'] = MAC
    tasks[1]['IP'] = IP

    task = list(filter(lambda tid: tid['id'] == task_id, tasks))
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task})


def exec_cmd(cmd):
    r = os.popen(cmd)
    text = r.read()
    r.close()
    return text


# curl -i -H "Content-Type: application/json" -X POST -d '{"title":"Read a book"}' http://localhost:5000/todo/api/v1.0/tasks
@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def task_post():

    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201


# curl -i http://localhost:5000/todo/api/v1.0/tasks/3
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    # All the computer can access this machine
    app.run(host='0.0.0.0', port=5000, debug=True)
    # app.run(debug=True)
