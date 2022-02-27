# Creating a database in flask
# Open terminal -> write python -> from app import db -> db.create_all() -> exit()
  
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy # using for database
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # to suppress the warning of SQLALCHEMY
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # for printing the object
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

# allows get and post request
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo) # for adding the changes
        db.session.commit() # for commit the changes
        
    allTodo = Todo.query.all() 
    return render_template('index.html', allTodo=allTodo) # for display all todo in index.html page

@app.route('/show')
def products():
    allTodo = Todo.query.all() # to fetch all the data from the database and print it.
    print(allTodo)
    return 'This is products page'

# allows get and post request
@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/") # redirecting to home page
        
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo) # for display todo in update.html page

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first() # delete first entry
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

# This will allow to run flask app
if __name__ == "__main__":
    app.run(debug=True, port=8000)