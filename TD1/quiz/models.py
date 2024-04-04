from .app import db
from sqlalchemy import delete

class Questionnaire(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String(100))

    def __init__(self , name):
        self.name = name

    def __repr__(self):
        return "<Questionnaire (%d) %s>" % (self.id , self.name)
    
    def to_json(self):
        json = {
            'id': self.id,
            'name': self.name,
            'questions': [question.to_json() for question in self.questions.all()]
        }
        return json

    def set_name(self , name):
        self.name = name

class Question(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    reponse = db.Column(db.String(120))
    question_type = db.Column(db.String(120))
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('questionnaire.id'))
    questionnaire = db.relationship ("Questionnaire", backref=db.backref("questions", lazy="dynamic"))

    __mapper_args__ = {
        'polymorphic_identity': 'question',
        'with_polymorphic': '*',
        'polymorphic_on': question_type
    }

    def __init__(self, title, question_type, questionnaire_id):
        self.title = title
        self.question_type = question_type
        self.questionnaire_id = questionnaire_id
    
    def to_json(self):
        json = {
            'questionnaire_id': self.questionnaire_id,
            'id': self.id,
            'title': self.title,
            'type': self.question_type,
            'answer': self.reponse
        }
        return json

class SimpleQuestion(Question):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'simple',
        'with_polymorphic': '*',
        'polymorphic_load': 'inline'
    }

    def __init__(self, title, reponse, questionnaire_id):
        super().__init__(title, "simple", questionnaire_id)
        self.reponse = reponse

class MultipleQuestion(Question):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    proposition1 = db.Column(db.String(120))
    proposition2 = db.Column(db.String(120))

    __mapper_args__ = {
        'polymorphic_identity': 'multiple',
        'with_polymorphic': '*',
        'polymorphic_load': 'inline'
    }

    def __init__(self, title, proposition1, proposition2, reponse, questionnaire_id):
        super().__init__(title, "multiple", questionnaire_id)
        self.proposition1 = proposition1
        self.proposition2 = proposition2
        self.reponse = reponse

    def to_json(self):
        json = super().to_json()
        json['proposition1'] = self.proposition1
        json['proposition2'] = self.proposition2
        return json


def get_questionnaires():
    return Questionnaire.query.all()

def get_questionnaire(id):
    return Questionnaire.query.get_or_404(id)

def create_questionnaire(name):
    questionnaire = Questionnaire(name)
    db.session.add(questionnaire)
    db.session.commit()
    return questionnaire

def update_questionnaire_name(id, name):
    get_questionnaire(id).set_name(name)
    db.session.commit()

def delete_questionnaire(id):
    deletion = get_questionnaire(id) # Pas besoin de "if questionnaire:" car get_or_404() le fait déjà
    db.session.delete(deletion)
    db.session.commit()


def get_questions(id_quiz):
    return get_questionnaire(id_quiz).questions.all()

def get_question(id_quiz, id_question):
    return get_questionnaire(id_quiz).questions.filter_by(id=id_question).first_or_404()

def update_question(id_quiz, id_question, requete):
    question = get_question(id_quiz, id_question)
    if requete.get('title'):
        question.title = requete['title']
    if requete.get('answer'):
        question.reponse = requete['answer']
    if requete.get('proposition1') and question.question_type == 'multiple':
        question.proposition1 = requete['proposition1']
    if requete.get('proposition2') and question.question_type == 'multiple':
        question.proposition2 = requete['proposition2']
    db.session.commit()
    return question

def create_simple_question(id_quiz, title, reponse):
    question = SimpleQuestion(title=title,
                              reponse=reponse,
                              questionnaire_id=id_quiz)
    db.session.add(question)
    db.session.commit()
    return question

def create_multiple_question(id_quiz, title, proposition1, proposition2, reponse):
    question = MultipleQuestion(title=title,
                                proposition1=proposition1,
                                proposition2=proposition2,
                                reponse=reponse,
                                questionnaire_id=id_quiz)
    db.session.add(question)
    db.session.commit()
    return question

def update_questionnaire_name(id, name):
    get_questionnaire(id).set_name(name)
    db.session.commit()

def delete_question(id_quiz, id_question):
    deletion = get_question(id_quiz, id_question) # Pas besoin de "if questionnaire:" car get_or_404() le fait déjà
    db.session.delete(deletion)
    db.session.commit()