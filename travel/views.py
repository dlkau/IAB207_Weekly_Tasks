from flask import Blueprint, render_template, request, redirect, url_for
from .models import Destination
from . import db


mainbp = Blueprint('main', __name__)

@mainbp.route('/')
def index():
    destinations = db.session.scalars(db.select(Destination)).all()
    return render_template("index.html", destinations=destinations)

# Define a search route
@mainbp.route('/search')
def search():
    if request.args["search"] and request.args["search"] != "":
        # Return the search command to the console
        print(request.args["search"])
        # Perform a query for the search term
        query_search = "%" + request.args["search"] + "%"
        destinations_match_query = db.session.scalars(db.select(Destination).where(Destination.description.like(query_search)))
        return render_template("index.html", destinations=destinations_match_query)
    else:
        return redirect(url_for('main.index'))

