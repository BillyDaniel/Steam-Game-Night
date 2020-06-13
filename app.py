import os
import re
import json
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
#relative path for sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

#initialize database
db = SQLAlchemy(app)
api_key = os.environ.get('STEAM_API_KEY')

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

@app.route('/login', methods=['POST','GET'])
def login():
    pass

#This will search for STEAM_ID and save it to a cookie
@app.route('/search', methods=['POST','GET'])
def search():
    if request.method == 'POST':
        search_content = request.form['name']
        try:
            pattern1 = 'http://steamcommunity.com/id/'
            pattern2 = 'http://steamcommunity.com/profile/'

            if search_content.startswith(pattern1):
                vanityurl = search_content[len(pattern1):]

                if vanityurl[len(vanityurl)-1] == '/':
                    vanityurl=vanityurl[:-1]


            elif search_content.startswith(pattern2):
                vanityurl = startswith[len(pattern2):]

                if vanityurl[len(vanityurl)-1] == '/':
                    vanityurl=vanityurl[:-1]

                response = request.get('http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/', params={'vanityurl':vanityurl})
                info = response.json()
                print(info)
                return render_template('search.html', infos = info)

        except:
            print("An Error has occured")
    else:
        return render_template('search.html')


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
