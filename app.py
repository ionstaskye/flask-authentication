from flask import Flask, render_template, redirect, request
from models import db, connect_db, User, AddUserForm, Feedback, LoginForm, AddFeedbackForm
from datetime import datetime
from flask_bcrypt import Bcrypt

app = Flask(__name__)

bcrypt= Bcrypt()
app.config['SECRET_KEY'] = "SecretSecret"

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


connect_db(app)
with app.app_context():db.create_all()

@app.route("/", methods = ["GET"])
def redirect_register():
    """Redirects user to register page"""

    return redirect("/register")

@app.route("/register", methods = ["GET","POST"])
def register_form():
    """Displays and submits register forms"""

    form = AddUserForm()

    if  form.validate_on_submit():
        
        username= form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)
        db.session.commit()
        session["user_id"] = new_user.id
        return redirect(f"/users/{new_user.username}")
    else:
        return render_template("registration.html", form = form)

app.route("/login", methods = ["GET","POST"])
def login_form():
    """Displays and submits login form"""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["user_id"] = user.id
            return redirect ("/secret")
        else:
            form.username.errors = ["Incorrect username or password"]
    return render_template("login.html", form = form)

app.route("/users/<username>/" methods =["GET"])
def secret_route(username):
    """displays secret route"""
    user = User.query.filter_by(username = username).first()
    feedback = Feedback.query.filter_by(created_by = user.id)
    if user_id  not in session:
        return redirect("/login")
    else:
        return render_template("user.html", user = user, feedback =feedback)

app.route("/logout")
def logout():
    """logouts the user and returns to login page"""

    session.pop("user_id")
    return redirect("/login")

app.route("/users/<username>/delete" methods = ["POST"])
def delete_user(username);
    """deletes user"""

    user = User.query.filter_by(username = username).first()

    db.session.delete(user)
    db.session.commit()

    return redirect("/")

app.route("/users/<username>/feedback/add" methods = ["GET", "POST"])
def feedback_add_form(username):
    "adds and submits feedback adding form"

    user = User.query.filter_by(username = username).first()
    form = AddFeedbackForm()

    if  form.validate_on_submit():
        
        title = form.title.data
        content = form.content.data
        created_by = user.id

        new_feedback = Feedback(title = title, content = content, created_by = created_by)

        db.session.add(new_feedback)
        db.session.commit()
        
        return redirect(f"/users/{username}")
    else:
        return render_template("add_feedback.html", form = form, user = user)    

app.route("/feedback/<int:feedback_id>/update" methods = ["GET", "POST"])
def feedback_edit(feedback_id):
    """Show and submit edit feedback form"""
    feedback = Feedback.query.get_or_404(feedback_id)
    if feedback.created_by != session["user_id"]:
        return redirect ("/")
    form = AddFeedbackForm()

    if  form.validate_on_submit():
        
        title = form.title.data
        content = form.content.data

        feedback.title = title
        feedback.content = content

        db.session.add(feedback)
        db.session.commit()
        
        return redirect(f"/users/{username}")
    else:
        return render_template("edit_feedback.html", form = form, feedback = feedback) 


  app.route("/feedback/<int:feedback_id>/delete" methods = ["POST"])
def feedback_edit(feedback_id):
    """Show and submit edit feedback form"""
    feedback = Feedback.query.get_or_404(feedback_id)
    if feedback.created_by != session["user_id"]:
        return redirect ("/")
    db.session.delte(feedback)
    db.session.commit()
    return redirect (f"/users/{feedback.username}")
