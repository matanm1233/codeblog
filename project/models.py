from flask_login import UserMixin, current_user
from . import db, create_app
from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for, flash
import flask_admin

# creates a user object which represents the user table in the sqlite database
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

# create a custom adminindexview class, the accessible method defines who is allowed to view the page
class MyAdminIndexView(flask_admin.AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated
    
    # if the user doesn't have access
    def inaccessible_callback(self, name, **kwargs):
        flash('Authentication Required')
        return redirect(url_for('main.index'))
