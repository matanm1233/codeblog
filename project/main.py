from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from . import db, create_app
from flask import session, Response
from .models import Post, User, Comment, PostLike
import datetime
from jinja2 import Template

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
    now = datetime.datetime.now()

    post = Post(title=title, post_content=textcontent, user_id=current_user.get_id(), created_at=now)
    db.session.add(post)
    db.session.commit()

    return redirect(url_for('main.index'))

@main.route('/addcomment/<post_title>', methods=['POST'])
@login_required
def addcomment(post_title):
    # get form content and find post
    comment_textcontent = request.form.get('comment')
    postid = Post.query.filter_by(title=post_title).first().id
    
    # create new comment object and add it to the database
    comment = Comment(post_content=comment_textcontent, post_id=postid, user_id=current_user.get_id(), created_at=datetime.datetime.now())
    db.session.add(comment)
    db.session.commit()
    return redirect(originurl(request))

@main.route('/<post_title>')
def read_post(post_title):
    # jank way of aligning url title with database title
    post_title = post_title.replace('-', ' ')

    article = Post.query.filter_by(title=post_title).first()
    return render_template('reader.html', post=article)

@main.route('/like/<post_title>')
@login_required
def like_post(post_title):
    post_title = post_title.replace('-', ' ')
    postid = Post.query.filter_by(title=post_title).first().id
    PostLikes = len(Post.query.filter_by(id=postid).first().likes)

    likes = Post.query.filter_by(title=post_title).first().likes
    for like in likes:
        if int(like.user_id) == int(current_user.get_id()):
            return unlike(like, postid)

    # check if the user has liked post before
    # create new like object based on user
    like = PostLike(created_at=datetime.datetime.now(), user_id=current_user.get_id(), post_id=postid)

    # commit to db
    db.session.add(like)
    db.session.commit()

    return redirect(originurl(request))

@main.route('/delcomment/<comment_id>')
@login_required
def remove_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        return redirect(url_for('main.index'))

    if not current_user.owns_comment(comment):
        return redirect(url_for('main.index'))

    db.session.delete(comment)
    db.session.commit()

    flash('Comment removed!')
    return redirect(originurl(request))


@main.route('/delpost/<post_title>')
@login_required
def remove_post(post_title):
    post_title = post_title.replace('-', ' ')
    post = Post.query.filter_by(title=post_title).first()
    
    if not post:
        return redirect(url_for('main.index'))

    if not current_user.owns_post(post):
        return redirect(url_for('main.index'))
    
    db.session.delete(post)
    db.session.commit()

    flash('Post removed!')
    return redirect(originurl(request))


def unlike(like, postid):
    db.session.delete(like)
    db.session.commit()
    
    return redirect(originurl(request))


def originurl(request):
    return request.headers['Referer']