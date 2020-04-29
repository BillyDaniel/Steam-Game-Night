import os
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
#relative path for sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

#initialize database
db = SQLAlchemy(app)
api_key = os.environ.get('STEAM_API')
#model for database
class Todo(db.Model):

    #primary key
    id = db.Column(db.Integer, primary_key=True)

    #string for task
    content = db.Column(db.String(200), nullable=False)

    #time task was created
    data_created = db.Column(db.DateTime, default=datetime.utcnow)

    #returns string when we create a new element (Id of task created)
    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Issue with adding task'
    else:
        tasks = Todo.query.order_by(Todo.data_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def deleteTask(id):
    delete_task = Todo.query.get_or_404(id)

    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect('/')
    except:
        return 'Issue with deleting task'

@app.route('/update/<int:id>', methods=['POST','GET'])
def updateTask(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task_content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'there was an issue updating task'
    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)
