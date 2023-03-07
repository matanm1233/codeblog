from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db, create_app
from flask import session

main = Blueprint('main', __name__)

# all our routes which don't require authentication

@main.route('/')
def index():
    try:
        admin = current_user.is_admin()
    except AttributeError:
        admin = False
    
    print(admin)
    return render_template("home.html", admin=admin)

@main.route('/profile')
@login_required
def profile():
    return render_template("profile.html", name=current_user.name)

