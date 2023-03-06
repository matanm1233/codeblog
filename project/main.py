from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db

main = Blueprint('main', __name__)

# all our routes which don't require authentication

@main.route('/')
def index():
    print(current_user.is_authenticated)
    return render_template("home.html")

@main.route('/profile')
@login_required
def profile():
    print(current_user)
    return render_template("profile.html", name=current_user.name)
