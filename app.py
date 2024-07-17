from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

# Initialize Flask application
app = Flask(__name__)
# Configure the SQLAlchemy database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# Initialize SQLAlchemy with Flask app
db = SQLAlchemy(app)


class Todo(db.Model):
    """
    Todo model for representing a to-do item in the database.

    Attributes:
        id (int): Unique identifier for the to-do item.
        content (str): The content of the to-do item.
        completed (bool): Status of the to-do item, True if completed, False otherwise.
        date_created (datetime): The date and time the to-do item was created.
    """
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        """Provide a string representation of the Todo item."""
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    """
    The index route that handles the creation and display of to-do items.

    Supports both GET and POST requests. On a GET request, it displays all to-do items.
    On a POST request, it adds a new to-do item to the database.

    Returns:
        On POST: Redirects to the index page to display the updated list of to-do items.
        On GET: Renders the index.html template with all to-do items passed as context.
    """
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Issue adding task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    """
    Route to delete a to-do item based on its id.

    Parameters:
        id (int): The unique identifier of the to-do item to be deleted.

    Returns:
        Redirects to the index page after deletion.
        If an issue occurs, returns a simple error message.
    """
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Issue deleting task'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    """
    Route to update the content of a to-do item.

    Supports both GET and POST requests. On a GET request, it displays the current content of the to-do item.
    On a POST request, it updates the content of the to-do item in the database.

    Parameters:
        id (int): The unique identifier of the to-do item to be updated.

    Returns:
        On POST: Redirects to the index page to display the updated list of to-do items.
        On GET: Renders the update.html template with the to-do item passed as context.
    """
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Issue updating task'
    else:
        return render_template('update.html', task=task)


if __name__ == '__main__':
    app.run(debug=True)