from flask import jsonify , abort , make_response , request, url_for
from .app import app
from .models import tasks, bd_get_tasks, bd_get_task, make_public_task, bd_add_task, bd_update_task


@app.route('/todo/api/v1.0/tasks', methods = ['GET'])
def get_tasks():
    return jsonify(tasks=bd_get_tasks())


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['GET'])
def get_task(task_id):
    return jsonify(task=bd_get_task(task_id))


@app.route('/todo/api/v1.0/tasks', methods = ['POST'])
def create_task():
    if not request .json or not 'title' in request.json:
        abort (400)
    task = {
        'title': request.json['title'],
        'description': request.json.get('description',""),
        'done': False
    }
    return jsonify (task = bd_add_task(task)),201

@app.errorhandler
def not_found(error):
    return make_response(
        jsonify (jsonify ({'error': 'Not found'})),
                 404
    )

@app.errorhandler
def not_found(error):
    return make_response(
        jsonify (jsonify ({'error': 'Bad Request'})),
                 400
    )

@app.route ('/todo/api/v1.0/tasks/<int:task_id>', methods = ['PUT'])
def update_task(task_id):
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != str:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not str:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort (400)
    update = {}
    json = request.json
    if 'title' in json:
        update ['title'] = json['title']
    if 'description' in json:
        update ['description'] = json['description']
    if 'done' in json:
        update ['done'] = json['done']
    return jsonify(bd_update_task(task_id, update))