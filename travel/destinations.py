from flask import Blueprint, render_template, request, redirect, url_for
from .models import Destination, Comment
from .forms import DestinationForm, CommentForm
from . import db
from werkzeug.utils import secure_filename
import os
from flask_login import login_required, current_user

# Use of blueprint to group routes, 
# name - first argument is the blue print name 
# import name - second argument - helps identify the root url for it 
destbp = Blueprint('destination', __name__, url_prefix='/destinations')

# Definition of helper functions
def check_upload_file(form):
  # Obtain the image data
  file_data = form.image.data
  file_name = file_data.filename

  # Create the upload path
  working_dir = os.path.dirname(__file__)
  file_upload_pth = os.path.join(working_dir, 'static/image/', secure_filename(file_name))
  # Store the relative apth in the database
  db_relative_pth = '/static/image/' + secure_filename(file_name)
  print(db_relative_pth)
  file_data.save(file_upload_pth)
  # Return the relative path back to the callers
  return db_relative_pth


@destbp.route('/<id>')
def show(id):
    # destination = get_destination()
    destination = db.session.scalar(db.select(Destination).where(Destination.id==id))
    cform = CommentForm()
    return render_template('destinations/show.html', destination=destination, form=cform)

@destbp.route('/create', methods = ['GET', 'POST'])
@login_required
def create():
  print('Method type: ', request.method)
  form = DestinationForm()
  if form.validate_on_submit():
    # Save the file
    db_relative_file_path = check_upload_file(form)
    destination = Destination(name=form.name.data,
                              description=form.description.data,
                              image=db_relative_file_path,
                              currency=form.currency.data)
    # Persist the data in the database
    db.session.add(destination)
    db.session.commit()
    print('Successfully created new travel destination')
    return redirect(url_for('destination.create'))
    # return redirect(url_for('destination.create'))
  return render_template('destinations/create.html', form=form)

def get_destination():
    brazilDescription = "Brazil is a picturesque country located in South America and is home to the largest " + \
    "rain forests in the world"
    img = "https://wallpapercave.com/wp/wp6843068.jpg"

    dest_brazil = Destination("Brazil", brazilDescription, img, "R$10")
    comment = Comment("Dylan", "What a beautiful country...", "2024-09-03 14:18:00:00")
    dest_brazil.add_comment(comment)
    comment = Comment("Bob", "Too noisy...", "2024-09-03 09:21:00:00")
    dest_brazil.add_comment(comment)
    comment = Comment("Sammantha", "I attended during their festivals. What an experience... ", "2023-08-02 12:54:12:00")
    dest_brazil.add_comment(comment)
    return dest_brazil



@destbp.route('/<id>/comment', methods = ['GET', 'POST'])
@login_required
def comment(id):
  # Here the form is created  form = CommentForm()
  form = CommentForm()
  # Retrieve the destiantion object sotred in the database
  destObj = db.session.scalar(db.select(Destination).where(Destination.id==id))
  if form.validate_on_submit():
    # Obtain the comment posted by the user and create the object to be commited
    user_comment = Comment(text=form.text.data, destination=destObj, user=current_user)
    db.session.add(user_comment)
    db.session.commit()
    print(f"The following comment has been posted: {form.text.data}")
  # notice the signature of url_for
  return redirect(url_for('destination.show', id=id))
