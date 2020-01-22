from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate(app, db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////exquisapp-todo.db'


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(150))
    done = db.Column(db.Boolean)


@app.route('/')
def index():
    not_done = Task.query.filter_by(done=False).all()
    done = Task.query.filter_by(done=True).all()

    return render_template('index.html',
                           not_done=not_done, done=done)


@app.route('/add', methods=['POST'])
def add():
    todo = Task(text=request.form['todoitem'], complete=False)
    db.session.add(todo)
    db.session.commit()


@app.route('/update/<:id>', methods=['PUT'])
def update(id):
    task = Task.query.filter_by(id=int(id)).first()
    task.task = request.form['todoitemm']
    db.session.add(todo)
    db.session.commit()
    return redirect


@app.route('/complete/<id>')
def complete(id):
    task = Task.query.filter_by(id=int(id)).first()
    task.done = True
    db.session.commit()

    return redirect(url_for('index'))


db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
