from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, FloatField, PasswordField
from wtforms.validators import InputRequired, Optional, NumberRange, URL, AnyOf
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db= SQLAlchemy()

class User (db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer,
                primary_key=True,
                autoincrement=True)
    username = db.Column(db.String(20),
                        nullable = False,
                        unique = True)
    password = db.Column(db.String(),
                        nullable = False,
                        )
    email = db.Column(db.String(50),
                        nullable=False
                        unique=True)
    first_name = db.Column(db.String(30),
                          nullable= False
                          )
    last_name = db.Column(db.String(30),
                          nullable= False
                          )
    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """ Registers user with hashed password"""

        hashed = bcrypt.generate_password_hash(password)

        hashed_utf = hashed.decode("utf8")

        return cls(username = username, password = hashed_utf, email = email, first_name = first_name, last_name = last_name)
    @classmethod
    def authenticate(cls, username, pwd):
        """authenticate user"""

        user = User.query.filter_by(username = username).first()

        if u and bcrypt.check_password_hash(user.password, pwd):
            return user
        else:
            return False

class AddUserForm(FlaskForm):

    username = StringField("Username", validators =[InputRequired(message = "Please input a username")])
    password = PasswordFieldField("Password", validators =[InputRequired(message = "Please input a password")])
    email = StringField("E-mail", validators =[InputRequired(message = "Please input a email")])
    first_name = StringField("First Name", validators =[InputRequired(message = "Please input a first name")])
    last_name = StringField("Last Name", validators =[InputRequired(message = "Please input a last name")])

class LoginFormForm(FlaskForm):

    username = StringField("Username", validators =[InputRequired(message = "Please input a username")])
    password = PasswordFieldField("Password", validators =[InputRequired(message = "Please input a password")])
    
class Feedback (db.Model):

    __tablename__ = "feedback"

    id = db.Column(db.Integer,
                primary_key=True,
                autoincrement=True)
    title = db.Column(db.String(100),
                        nullable = False)
    content = db.Column(db.String(),
                        nullable = False)
    created_by = db.Column(
                            db.ForeignKey('users.id'))

    user = db.relationship("User", backref = "feedback")

class AddFeedbackForm(FlaskForm):

    title = StringField("Title", validators =[InputRequired(message = "Please input a title")])
    content = StringField("Content", validators =[InputRequired(message = "Please input content")])

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
