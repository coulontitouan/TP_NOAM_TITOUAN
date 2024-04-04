from .app import app
import quiz.models as md
from flask import jsonify, abort, make_response, request, url_for


@app.route('/quiz/api/v1.0/quiz', methods = ['GET'])
def get_questionnaires():
    res = []
    for quiz in md.get_questionnaires():
        res.append(quiz.to_json())
    return jsonify(res)

@app.route('/quiz/api/v1.0/quiz/<int:quiz_id>', methods = ['GET'])
def get_questionnaire(quiz_id):
    print(md.get_questionnaire(quiz_id).to_json())
    return jsonify(md.get_questionnaire(quiz_id).to_json())

@app.route('/quiz/api/v1.0/quiz', methods = ['POST'])
def create_questionnaire():
    if not request.json or 'name' not in request.json:
        abort(400)
    questionnaire = md.create_questionnaire(request.json['name']).to_json()
    return jsonify({'quiz': questionnaire}), 201


@app.route('/quiz/api/v1.0/quiz/<int:quiz_id>', methods = ['PUT'])
def update_questionnaire(quiz_id):
    if not request.json:
        abort(400)
    if 'name' not in request.json or ('name' in request.json and not isinstance(request.json['name'], str)):
        abort(400)
    md.update_questionnaire_name(quiz_id, request.json['name'])
    return jsonify(md.get_questionnaire(quiz_id).to_json())

@app.route('/quiz/api/v1.0/quiz/<int:quiz_id>', methods = ['DELETE'])
def delete_questionnaire(quiz_id):
    md.delete_questionnaire(quiz_id)
    return jsonify({'deletion': True})

@app.route('/quiz/api/v1.0/quiz/<int:quiz_id>/questions', methods = ['GET'])
def get_questions(quiz_id):
    res = []
    for question in md.get_questions(quiz_id):
        res.append(question.to_json())
    return jsonify(res)


@app.route('/quiz/api/v1.0/quiz/<int:quiz_id>/questions/<int:question_id>', methods = ['GET'])
def get_question(quiz_id, question_id):
    return jsonify(md.get_question(quiz_id, question_id).to_json())


@app.route('/quiz/api/v1.0/quiz/<int:quiz_id>/questions', methods = ['POST'])
def create_question(quiz_id):
    if not request.json or 'type' not in request.json:
        abort(400)
    match request.json['type']:
        case 'simple':
            if 'title' not in request.json or 'answer' not in request.json:
                abort(400)
            question = md.create_simple_question(quiz_id, request.json['title'], request.json['answer']).to_json()
        case 'multiple':
            if 'title' not in request.json or 'proposition1' not in request.json or 'proposition2' not in request.json or 'answer' not in request.json:
                abort(400)
            question = md.create_multiple_question(quiz_id, request.json['title'], request.json['proposition1'], request.json['proposition2'], request.json['answer']).to_json()
        case _:
            abort(400)
    return jsonify({'question created': question}), 201


@app.route('/quiz/api/v1.0/quiz/<int:quiz_id>/questions/<int:question_id>', methods = ['PUT'])
def update_question(quiz_id, question_id):
    if not request.json:
        abort(400)
    question = md.update_question(quiz_id, question_id, request.json).to_json()
    return jsonify({'question updated': question})


@app.route('/quiz/api/v1.0/quiz/<int:quiz_id>/questions/<int:question_id>', methods = ['DELETE'])
def delete_question(quiz_id, question_id):
    md.delete_question(quiz_id, question_id)
    return jsonify({'deletion': True})
