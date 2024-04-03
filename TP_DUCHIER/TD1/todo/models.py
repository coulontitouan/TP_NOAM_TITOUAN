from flask import jsonify , abort , make_response , request, url_for

tasks = [
    {
    'id': 1,
    'title': 'Courses',
    'description': 'Salade, Oignons, Pommes, Clementines',
    'done': True
    },

    {
    'id': 2,
    'title': 'Apprendre REST',
    'description': 'Apprendre mon cours et comprendre les exemples',
    'done': False
    },

    {
    'id': 3,
    'title': 'Apprendre Ajax',
    'description': 'Revoir les exemples et ecrire un client REST JS avec Ajax',
    'done': False
    }
]

def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task ['uri'] = url_for (
                'get_task', 
                task_id = task['id'],
                _external = True)
        else:
            new_task [field] = task[field]
    return new_task

def bd_get_tasks():
    return [make_public_task(t) for t in tasks]

def _get_task(task_id):
    for task in tasks:
        if task.get('id', None) == task_id:
            return task
    abort(404)

def bd_get_task(task_id):
    return make_public_task(_get_task(task_id))

def bd_add_task(task):
    task['id'] = tasks[-1]['id'] + 1 if tasks else 1
    tasks.append(task)
    return make_public_task(task)
#curl -X POST -H "Content-Type: application/json" http://127.0.0.1:5000/todo/api/v1.0/tasks -d '{"title":"hello", "description":"blablabla"}'

def bd_update_task(task_id, update):
    task = _get_task(task_id)
    for k,v in update.items():
        task[k] = v
    return make_public_task(task)
#curl -X PUT -H "Content-Type: application/json" http://127.0.0.1:5000/todo/api/v1.0/tasks/2 -d '{"done" : true}'
