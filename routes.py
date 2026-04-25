from flask import request, redirect, url_for, render_template
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps
from datetime import datetime
from models import db, User, Project, Story, Task


#To seperate the roles of normal user and manager/admin
def role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.role != role:
                return "Access Denied"
            return func(*args, **kwargs)
        return wrapper
    return decorator



def init_routes(app):

    @app.route("/")
    def home():
        return redirect(url_for("login"))
    
    #Login Page
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            user = User.query.filter_by(
                username=request.form.get("username")
            ).first()

            if user and user.password == request.form.get("password"):
                login_user(user)
                return redirect(url_for("dashboard"))

            return "Invalid credentials"

        return render_template("login.html")

    #Dashboard Welcome
    @app.route("/dashboard")
    @login_required
    def dashboard():
        return render_template("dashboard.html")

    
    #Creating a Project interface
    @app.route("/create_project", methods=["GET", "POST"])
    @login_required
    @role_required("manager")
    def create_project():
        if request.method == "POST":
            project = Project(
                name=request.form.get("name"),
                description=request.form.get("description"),
                due_date=datetime.strptime(request.form.get("due_date"), "%Y-%m-%d")
            )
            db.session.add(project)
            db.session.commit()
            return redirect(url_for("dashboard"))

        return render_template("create_project.html")


    #Details about the projects (View)
    @app.route("/view_projects")
    @login_required
    def view_projects():
        projects = Project.query.all()
        return render_template("view_projects.html", projects=projects)


    #View a single project with the ID
    @app.route("/project/<int:project_id>")
    @login_required
    def view_project(project_id):
        project = Project.query.get_or_404(project_id)
        stories = Story.query.filter_by(project_id=project_id).all()
        return render_template("project_detail.html", project=project, stories=stories)
    
    #Create a story in project
    @app.route("/create_story/<int:project_id>", methods=["GET", "POST"])
    @login_required
    @role_required("manager")
    def create_story(project_id):
        if request.method == "POST":
            title = request.form.get("title")

            story = Story(
                title=title,
                project_id=project_id,
                status="To Do"
            )

            db.session.add(story)
            db.session.commit()

            return redirect(url_for("view_project", project_id=project_id))

        return render_template("create_story.html", project_id=project_id)
    
    #Each Story detail with ID
    @app.route("/story/<int:story_id>")
    @login_required
    def view_story(story_id):
        story = Story.query.get_or_404(story_id)
        tasks = Task.query.filter_by(story_id=story_id).all()
        users = User.query.all()

        return render_template("story_detail.html", story=story, tasks=tasks, users=users)
    
    
    #Create tasks but only manager role allowed
    @app.route("/create_task/<int:story_id>", methods=["GET", "POST"])
    @login_required
    @role_required("manager")
    def create_task(story_id):

        users = User.query.all()

        if request.method == "POST":
            title = request.form.get("title")
            assigned_to = request.form.get("assigned_to")

            task = Task(
                title=title,
                story_id=story_id,
                assigned_to=int(assigned_to),
                status="To Do"
            )

            db.session.add(task)
            db.session.commit()

            return redirect(url_for("view_story", story_id=story_id))

        return render_template("create_task.html", users=users)

    @app.route("/update_task/<int:task_id>/<string:new_status>")
    @login_required
    @role_required("manager")
    def update_task(task_id, new_status):
        task = Task.query.get_or_404(task_id)
        task.status = new_status
        db.session.commit()
    
        # --- Update Story ---
        story = Story.query.get(task.story_id)
        tasks = Task.query.filter_by(story_id=story.id).all()
    
        if all(t.status == "Done" for t in tasks):
            story.status = "Done"
        else:
            story.status = "In Progress"
    
        db.session.commit()
    
        # --- Update Project ---
        project = Project.query.get(story.project_id)
        stories = Story.query.filter_by(project_id=project.id).all()
    
        if all(s.status == "Done" for s in stories):
            project.status = "Done"
        else:
            project.status = "In Progress"
    
        db.session.commit()
    
        return redirect(url_for("view_story", story_id=story.id))


    #Redirect to login after logout
    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("login"))