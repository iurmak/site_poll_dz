from app.py import db

class Ans(db.Model):
    __tablename__ = "answers"

    a_id = db.Column('a_id', db.Integer, primary_key=True)
    text = db.Column('text', db.Text)

class Que(db.Model):
    __tablename__ = "questions"

    q_id = db.Column('q_id', db.Integer, primary_key=True)
    text = db.Column('text', db.Text)

class Res(db.Model):
    __tablename__ = "responds"

    q_id = db.Column('q_id', db.Integer, primary_key=False)
    u_id = db.Column('u_id', db.Integer, primary_key=False)
    a_id = db.Column('a_id', db.Integer, primary_key=False)

    answer = db.relationship('answers', uselist=False, primaryjoin="responds.a_id==answers.a_id")
    person = db.relationship('Ui', uselist=False, primaryjoin="responds.u_id==user_info.u_id")
    question = db.relationship('questions', uselist=False, primaryjoin="responds.q_id==questions.q_id")

class Ui(db.Model):
    __tablename__ = "user_info"

    u_id = db.Column('u_id', db.Integer, primary_key=True)
    name = db.Column('name', db.Text)
    age = db.Column('age', db.Text)
    place = db.Column('place', db.Text)
    edu = db.Column('edu', db.Text)