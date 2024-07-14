from app import app, db  # Import the Flask application and the SQLAlchemy instance

# Create an application context
with app.app_context():
    # Now you can safely call methods that require the application context
    db.create_all()  # This will create the database and tables