from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from . import db, create_app
from flask import session
from .models import Post, User

main = Blueprint('main', __name__)

# all our routes which don't require authentication

@main.route('/')
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    
    return render_template("home.html", posts=posts)

@main.route('/profile')
@login_required
def profile():
    return render_template("profile.html", name=current_user.name)

@main.route('/addpost', methods=['POST'])
def addpost():
    textcontent = request.form.get('postcontent')
    title = request.form.get('title')

    # make sure content is not empty
    if not textcontent or not title:
        flash("Must enter all fields!")
        return redirect(url_for('main.index'))
    
    # otherwise add to the db
    import datetime

    now = datetime.datetime.now()

    post = Post(title=title, post_content=textcontent, user_id=current_user.get_id(), created_at=now)
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('main.index'))

