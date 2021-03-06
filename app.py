from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String())
    done = db.Column(db.Boolean)


@app.route('/')
def index():
    not_done = Task.query.filter_by(done=False).all()
    done = Task.query.filter_by(done=True).all()

    return render_template('index.html',
                           not_done=not_done, done=done)


@app.route('/add', methods=['POST'])
def add():
    if request.form['todoitem'] == '':
        pass
    else:
        todo = Task(task=request.form['todoitem'], done=False)
        db.session.add(todo)
        db.session.commit()
        db.session.close()

    return redirect(url_for('index'))


@app.route('/update/<id>', methods=['POST'])
def update(id):
    task = Task.query.filter_by(id=int(id)).first()
    task.task = request.form['todoitem']
    db.session.add(task)
    db.session.commit()
    db.session.close()

    return redirect(url_for('index'))


@app.route('/delete/<id>')
def delete(id):
    Task.query.filter_by(id=int(id)).delete()
    db.session.commit()
    db.session.close()

    return redirect(url_for('index'))


@app.route('/edit/<id>')
def edit(id):
    task = Task.query.filter_by(id=int(id)).first()

    return render_template('edit.html',
                           task=task)


@app.route('/complete/<id>')
def complete(id):
    task = Task.query.filter_by(id=int(id)).first()
    task.done = True
    db.session.commit()

    return redirect(url_for('index'))


db.create_all()

if __name__ == '__main__':
    app.run()
