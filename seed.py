from app import app, db
from models import User

with app.app_context():
    # Reset DB
    db.drop_all()
    db.create_all()

    # Create users
    admin = User(username="admin", password="admin123", role="admin")
    manager = User(username="manager", password="123", role="manager")
    viewer = User(username="viewer", password="123", role="viewer")

    db.session.add_all([admin, manager, viewer])
    db.session.commit()

    print("Database reset and users created!")