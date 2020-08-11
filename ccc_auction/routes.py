from ccc_auction import app, db
from flask import render_template, url_for, flash, redirect
from ccc_auction.forms import LoginForm, PlaceBid
from ccc_auction.models import Bidder, Item
from flask_login import login_user, current_user, logout_user, login_required
from ccc_auction.routes_displayItems_helper import *

@app.route("/", methods = ["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('displayItems'))
    form = LoginForm()
    if form.validate_on_submit():
        # Grab the bidder's ID from the database
        bidder = Bidder.query.filter_by(biddername=form.biddername.data).first()
        # Show the 'items' page if login info is correct
        if bidder and bidder.id == form.password.data:
            login_user(bidder, remember=form.remember.data)
            return redirect(url_for('displayItems'))
        else:
            flash('Login Unsuccessful. Please check your name and ID', 'danger')
            
    return render_template("login.html", title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('displayItems'))

@app.route("/items", methods=['GET', 'POST'])
@login_required
def displayItems():
    # z variables contain tuples of the form (item_group, form_group)
    z1, z2, z3, items, forms = gatherForms()

    # Trigger a bid if button is clicked
    for form in forms:
        if form.submit.data and form.validate_on_submit():
            placeBidUpdateDatabase(form)
            return redirect(url_for('displayItems'))

    return render_template("items.html", items=items, z1=z1, z2=z2, z3=z3)