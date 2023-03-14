from flask_login import UserMixin, current_user, AnonymousUserMixin
from . import db, create_app
from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for, flash
import flask_admin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

# creates a user object which represents the user table in the sqlite database
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    hash = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    admin = db.Column(db.Boolean)

    # relationships
    posts = db.relationship('Post', backref='user')
    comments = db.relationship('Comment', backref='user')

    def is_admin(self):
         return self.admin
    
    def owns_post(self, post):
         return post.user_id == self.id

    def owns_comment(self, comment):
         return comment.user_id == self.id
    
    
class Post(db.Model):
     id = db.Column(db.Integer, primary_key = True)
     title = db.Column(db.String(100), unique=True, nullable=False)
     post_content = db.Column(db.Text)
     created_at = db.Column(db.DateTime)
    
    # relationships
     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
     comments = db.relationship('Comment', backref='post')
     likes = db.relationship('PostLike', backref='post')
     column_display_pk = True # optional, but I like to see the IDs in the list
     column_hide_backrefs = False



class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    post_content = db.Column(db.Text)
    created_at = db.Column(db.DateTime)

    # relationships
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class PostLike(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    created_at = db.Column(db.DateTime)

    # relationships
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class AdminModelView(ModelView):
        column_hide_backrefs = True
        column_display_pk = True # optional, but I like to see the IDs in the list

# create a custom adminindexview class, the accessible method defines who is allowed to view the page
class MyAdminIndexView(flask_admin.AdminIndexView):
    def is_accessible(self):
        return current_user.is_admin()
    
    # if the user doesn't have access
    def inaccessible_callback(self, name, **kwargs):
        flash('Forbidden: Not an Admin')
        return redirect(url_for('main.index'))

class AnonymousUser(AnonymousUserMixin):
     def is_admin(self):
          return False
     
     def get_id(self):
          return None
     
     def owns_post(self, post):
          return False

     def owns_comment(self, comment):
          return False