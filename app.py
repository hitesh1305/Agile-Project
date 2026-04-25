from flask import Flask
from flask_login import LoginManager
from models import db, User, Project
from routes import init_routes
import os
import threading
import time
from datetime import datetime


# -------------------- APP SETUP --------------------

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your-secret-key'

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db.init_app(app)


# -------------------- LOGIN SETUP --------------------

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# -------------------- ROUTES --------------------

init_routes(app)


# -------------------- BACKGROUND TASK --------------------

def check_deadlines(app):
    with app.app_context():
        while True:
            projects = Project.query.all()

            for project in projects:
                if project.due_date and project.status != "Done":
                    if datetime.now() > project.due_date:
                        project.status = "Overdue"

            db.session.commit()
            print("Checked deadlines...")
            time.sleep(30)


def start_background_thread(app):
    thread = threading.Thread(target=check_deadlines, args=(app,))
    thread.daemon = True
    thread.start()


# -------------------- DB INIT + SEED --------------------

with app.app_context():
    db.create_all()

    # Seed users if DB is empty
    if not User.query.first():
        admin = User(username="admin", password="admin123", role="admin")
        manager = User(username="manager", password="123", role="manager")
        viewer = User(username="viewer", password="123", role="viewer")

        db.session.add_all([admin, manager, viewer])
        db.session.commit()


# Start background thread (works locally + Render)
start_background_thread(app)


# -------------------- RUN --------------------

if __name__ == "__main__":
    app.run(debug=True)