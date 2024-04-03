from .app import db
from flask import url_for

class Questionnaire(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Questionnaire (%d) %s>" % (self.id, self.name)

    def to_json(self):
        json={
            'quiz_id': self.id,
            'id': self.id,
            'name': self.name,
            'url': url_for('get_quiz',quiz_id=self.id, _external=True),
            'questions': [q.to_json() for q in self.questions.all()]
        }
        return json

class Question(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    #questionType = db.Column(db.String(120))
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('questionnaire.id'))
    questionnaire = db.relationship("Questionnaire", 
        backref = db.backref("questions", lazy="dynamic"))
    
    def __repr__(self):
        return f"<Question{self.id} {self.title}>"
    
    def to_json(self):
        json={
            'url': url_for('get_question', question_id = self.id, _external = True),
            'quiz_url':  url_for('get_quiz', quiz_id = self.questionnaire_id, _external = True),
            'title': self.title
        }
        return json

def db_get_all_quiz():
    return Questionnaire.query.all()
def db_get_quiz(quiz_id):
    return Questionnaire.query.get_or_404(quiz_id)

def db_get_all_question():
    return Question.query.all()

def db_get_question(question_id):
    return Question.query.get_or_404(question_id)

def db_create_quiz(json):
    quiz = Questionnaire(name=json['name'])
    db.session.add(quiz)
    db.session.commit()
    return quiz

def db_create_question(json):
    question = Question(
        title=json['title'],
        questionnaire_id=json['quiz_id']
    )
    db.session.add(question)
    db.session.commit()
    return question

def db_delete_quiz(quiz_id):
    quiz = Questionnaire.query.get_or_404(quiz_id)
    db.session.delete(quiz)
    db.session.commit()
    return {"status": "success"}

def db_update_quiz(quiz_id, data):
    quiz = Questionnaire.query.get_or_404(quiz_id)
    quiz.name = data['name']
    db.session.commit()
    return quiz

def db_update_question(question_id, data):
    question = Question.query.get_or_404(question_id)
    question.title = data['title']
    db.session.commit()
    return question

def db_delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    return {"status": "success"}


#curl -i -H "Content-Type: application/json" -X POST -d '{"name":"MonQuiz1"}' http://localhost:5000/quiz/api/v1.0/quiz

#curl -i -H "Content-Type: application/json" -X POST -d '{"quiz_id":"1", "title" :"question n1"}' http://localhost:5000/quiz/api/v1.0/question