from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import LoginForm, RegisterForm
from flask_login import login_user, login_required, logout_user
from flask_bcrypt import generate_password_hash, check_password_hash
from .models import User
from . import db

# Define a new blueprint
authbp = Blueprint("auth", __name__)

@authbp.route('/login', methods=["GET", "POST"])
def login():
    loginForm = LoginForm()
    # Define a varaible setting error to None
    error = None
    if loginForm.validate_on_submit() == True:
        # Retrieve information from the form
        userName = loginForm.user_name.data
        password = loginForm.password.data
        user = db.session.scalar(db.select(User).where(User.name==userName))
        # Ensure there is a user with the name
        if user is None:
            error = 'Incorrect Username Provided'
        elif not check_password_hash(user.pass_hash, password):
            error = 'Incorrect Password'
        # Check if there is no error
        if error is None:
            # Allow the user to be logged in and redirect them
            login_user(user)
            return redirect(url_for('main.index'))
        # If there is an error, flash the message to the user
        else:
            flash(error)
    return render_template('user.html', form=loginForm, heading='Login')

@authbp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Retrieve the information from the form
        userName = form.user_name.data
        password = form.password.data
        email = form.email_id.data
        # Ensure that the does not exist in the db already
        user = db.session.scalar(db.select(User).where(User.name==userName))
        # If the user exists redirect them
        if user:
            flash("A user with that username already exsits.")
            return redirect(url_for('auth.register'))
        # Hash the password
        password_hash = generate_password_hash(password)
        # Create a new user object
        registeredUser = User(name=userName, pass_hash=password_hash, email_id=email)
        db.session.add(registeredUser)
        db.session.commit()
        # Return the the main index page
        return redirect(url_for('main.index'))
    else:
        return render_template('user.html', form=form, heading="Register")
    
@authbp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))