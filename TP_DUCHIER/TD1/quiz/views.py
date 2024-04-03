from .app import app
from .models import (
    db_delete_question,
    db_delete_quiz,
    db_get_all_quiz, 
    db_get_quiz, 
    db_get_all_question, 
    db_get_question, 
    db_create_quiz, 
    db_create_question,
    db_update_quiz, 
    db_update_question
)
from flask import jsonify, request, abort, url_for

# Routes pour CRUD sur les quizzes
@app.route('/quiz/api/v1.0/quiz', methods=["GET"])
def get_all_quiz():
    quizzes = db_get_all_quiz()
    return jsonify([q.to_json() for q in quizzes])

@app.route('/quiz/api/v1.0/quiz/<int:quiz_id>', methods=["GET"])
def get_quiz(quiz_id):
    quiz = db_get_quiz(quiz_id)
    if not quiz:
        abort(404)
    return jsonify(quiz.to_json())

@app.route('/quiz/api/v1.0/quiz', methods=["POST"])
def create_quiz():
    data = request.json
    if not data or 'name' not in data:
        abort(400)
    quiz = db_create_quiz(data)
    return jsonify(quiz.to_json()), 201

@app.route('/quiz/api/v1.0/quiz/<int:quiz_id>', methods=["PUT"])
def update_quiz(quiz_id):
    quiz = db_get_quiz(quiz_id)
    if not quiz:
        abort(404)
    data = request.json
    if not data or 'name' not in data:
        abort(400)
    quiz = db_update_quiz(quiz_id, data)
    return jsonify(quiz.to_json())

@app.route('/quiz/api/v1.0/quiz/<int:quiz_id>', methods=["DELETE"])
def delete_quiz(quiz_id):
    result = db_delete_quiz(quiz_id)
    if not result:
        abort(404)
    return jsonify({'message': 'Quiz deleted successfully'})


# Routes pour CRUD sur les questions
@app.route('/quiz/api/v1.0/question', methods=["GET"])
def get_all_question():
    questions = db_get_all_question()
    return jsonify([q.to_json() for q in questions])

@app.route('/quiz/api/v1.0/question/<int:question_id>', methods=["GET"])
def get_question(question_id):
    question = db_get_question(question_id)
    if not question:
        abort(404)
    return jsonify(question)

@app.route('/quiz/api/v1.0/question', methods=["POST"])
def create_question():
    data = request.json
    if not data or 'quiz_id' not in data or 'title' not in data:
        abort(400)
    question = db_create_question(data)
    return jsonify(question.to_json()), 201

from flask import jsonify, request, abort, url_for
from .models import db, Question

# Route pour mettre à jour le nom d'une question
@app.route('/quiz/api/v1.0/question/<int:question_id>', methods=["PUT"])
def update_question(question_id):
    question = Question.query.get(question_id)
    if not question:
        abort(404)
    data = request.json
    if not data or 'title' not in data:
        abort(400)
    question.title = data['title']
    db.session.commit()
    return jsonify({'message': 'Question updated successfully'})


@app.route('/quiz/api/v1.0/question/<int:question_id>', methods=["DELETE"])
def delete_question(question_id):
    result = db_delete_question(question_id)
    if not result:
        abort(404)
    return jsonify({'message': 'Question deleted successfully'})
