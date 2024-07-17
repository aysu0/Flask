from flask import Flask, render_template, url_for, request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.DateTime, nullable=True)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Task %r>' % self.id



@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST': #checks if request method is POST
        task_content = request.form['content']
        task_deadline = request.form['deadline']
        if task_deadline:
            task_deadline = datetime.strptime(task_deadline, '%Y-%m-%d')
        new_task = ToDo(content=task_content, deadline=task_deadline)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = ToDo.query.order_by(ToDo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    taskToDelete = ToDo.query.get_or_404(id)
    try:
        db.session.delete(taskToDelete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting this task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = ToDo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        task.deadline = request.form['deadline'] 
        if task.deadline:
            task.deadline = datetime.strptime(task.deadline, '%Y-%m-%d')
            task.completed = 'completed' in request.form
        try: 
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)

migrate = Migrate(app, db)

@app.route('/complete/<int:id>', methods=['POST'])
def complete(id):
    task = ToDo.query.get_or_404(id)
    task.completed = not task.completed  # Toggle the completed status

    try:
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem marking this task as completed'


if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()  # Create the database tables
    app.run(debug=True)

