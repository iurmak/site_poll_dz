from flask import Flask, request, render_template, redirect,\
    url_for, flash, Markup
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = '228'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dialectal_poll.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Answers(db.Model):
    a_id = db.Column(db.Integer, primary_key=True)
    a_text = db.Column(db.Text)


class Questions(db.Model):
    q_id = db.Column(db.Integer, primary_key=True)
    q_text = db.Column(db.Text)
    c_a = db.Column(db.Integer, db.ForeignKey('answers.a_id'))


class responses(db.Model):
    r_id = db.Column(db.Integer, primary_key=True)
    q_id = db.Column(db.Integer, db.ForeignKey('questions.q_id'))
    a_id = db.Column(db.Integer, db.ForeignKey('answers.a_id'))
    u_id = db.Column(db.Integer, db.ForeignKey('users.u_id'))


class Users(db.Model):
    u_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    age = db.Column(db.Text)
    place = db.Column(db.Text)
    edu = db.Column(db.Text)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/poll')
def poll():
    return render_template('poll.html')


@app.route('/results')
def res():
    def q(q_id):
        return (str([i for i in db.session.execute("""SELECT
            a_text
            FROM responses
                JOIN answers ON answers.a_id = responses.a_id
            WHERE q_id = %d
            GROUP BY responses.a_id
            ORDER BY COUNT(q_id) DESC
            LIMIT 1""" % q_id)][0][0]))

    def p(ans, q_id):
        return (int([i for i in db.session.execute("""SELECT
            (COUNT(CASE a_id WHEN %d THEN 1 ELSE null END) * 1./ COUNT(a_id)) * 100
            FROM responses
            WHERE q_id = % d""" % (int(Questions.query.filter_by(q_id=q_id).first().c_a), q_id))][0][0]))

    if not [i for i in db.session.execute("""SELECT a_id FROM responses""")]:
        flash('Будьте первопроходцем – ответьте на вопросы, чтобы получить статистику.', ' alert-danger')
        return redirect(url_for('poll'))

    total = int(*[i for i in db.session.execute("SELECT COUNT(r_id) / 3 FROM responses")][0])
    average = int(*[i for i in db.session.execute("SELECT AVG(age) FROM users")][0])
    pob_f = [i for i in db.session.execute(
        """SELECT place
        FROM users
        GROUP BY place
        ORDER BY COUNT(age) DESC
        LIMIT 1
        """)][0][0]
    edu = [i for i in db.session.execute(
        """SELECT edu
        FROM users
        GROUP BY edu
        ORDER BY COUNT(edu) DESC
        LIMIT 1
        """)][0][0]

    q1_f = q(1)
    q2_f = q(2)
    q3_f = q(3)
    q1_p = p(1, 1)
    q2_p = p(2, 2)
    q3_p = p(1, 3)

    return render_template('results.html',
                           total=total,
                           average=average,
                           pob_f=pob_f,
                           edu=edu,
                           q1_f=q1_f,
                           q2_f=q2_f,
                           q3_f=q3_f,
                           q1_p=q1_p,
                           q2_p=q2_p,
                           q3_p=q3_p)


@app.route('/process', methods=['POST'])
def process():
    name = request.form.get('user')
    age = request.form.get('age', type=int)
    place = request.form.get('pob')
    edu = request.form.get('ed')
    user = Users(name=name,
                 age=age,
                 place=place,
                 edu=edu)
    db.session.add(user)
    db.session.commit()

    user_id = user.u_id
    resp1 = request.form.get('q1')
    resp2 = request.form.get('q2')
    resp3 = request.form.get('q3')
    ans1 = responses(q_id=1,
                    u_id=user_id,
                    a_id=resp1)
    ans2 = responses(q_id=2,
                    u_id=user_id,
                    a_id=resp2)
    ans3 = responses(q_id=3,
                    u_id=user_id,
                    a_id=resp3)
    for i in [ans1, ans2, ans3]:
        db.session.add(i)
    db.session.commit()
    flash(Markup('Спасибо за участие в опросе!<br>Если хотите, ознакомьтесь с текущей статистикой.'), 'alert alert-success')
    return redirect(url_for("res"))


if __name__ == '__main__':
    app.run(debug=True, port=8000)
