from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import flask_login
from flask_login import LoginManager, current_user
from jinja2 import Environment, PackageLoader, select_autoescape
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

# this is the app factory


# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    
    # this adds the view which can edit the User table
    from .models import User, MyAdminIndexView

    # init admin page
    app.config['FLASK_ADMIN_SWITCH'] = 'cerulean'
    admin = Admin(app, name='Blog Admin', index_view=MyAdminIndexView())


    admin.add_view(ModelView(User, db.session))


    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    # initialize database
    db.init_app(app)
    
    # initialize flask-login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    # initialize login features
    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
    
    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

