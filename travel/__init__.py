from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import datetime


db = SQLAlchemy()

# Define a constant where the images are saved
UPLOAD_FOLDER = '/static/image'

def create_app():
    app = Flask(__name__)

    # we use this utility module to display forms quickly
    Bootstrap(app)

    # A secret key for the session object
    app.secret_key = 'somerandomvalue'

    # Configure the Database URI
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///traveldb.sqlite"
    db.init_app(app)

    # Create a new Login manager object
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    # Import User from Models
    from .models import User
    @login_manager.user_loader
    def load_curr_user(user_id):
        return db.session.scalar(db.select(User).where(User.id==user_id))

    
    # Configure the location where the images are saved
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
    # Add Blueprints
    from . import views
    app.register_blueprint(views.mainbp)
    from . import destinations
    app.register_blueprint(destinations.destbp)
    from . import auth
    app.register_blueprint(auth.authbp)

    # Include an app errorhandler for 404 errors
    @app.errorhandler(404)
    def page_not_found(err):
        return render_template("404.html", error=err)


    return app