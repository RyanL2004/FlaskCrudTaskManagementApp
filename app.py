from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# Modified Todo model in app.py
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    priority = db.Column(db.String(20), default='Medium')  # High, Medium, Low
    completed = db.Column(db.Boolean, default=False)
    description = db.Column(db.Text)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        task_priority = request.form['priority']
        task_due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d') if request.form['due_date'] else None
        
        new_task = Todo(
            content=task_content,
            priority=task_priority,
            due_date=task_due_date
        )

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except: 
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)
    
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting the task'
    
@app.route('/update/<int:id>', methods = ['GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task_content = request.form['content']
        task.content = task_content

        try: 
            db.session.commit()
            return redirect('/')
        except:
            return 'there was an issue updating your task'
    
    else:
        return render_template('update.html', task = task)

@app.route('/toggle/<int:id>')
def toggle_complete(id):
    task = Todo.query.get_or_404(id)
    task.completed = not task.completed
    try:
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue updating the task'
    

if __name__ == "__main__":
    app.run(debug=True)