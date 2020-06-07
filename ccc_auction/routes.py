from ccc_auction import app, db, bcrypt
from flask import render_template, url_for, flash, redirect
from ccc_auction.forms import LoginForm
from ccc_auction.models import Bidder, Item
from flask_login import login_user


@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/", methods = ["GET", "POST"])
def logIn():
    form = LoginForm()
    if form.validate_on_submit():
        bidder = Bidder.query.filter_by(biddername=form.biddername.data).first()
        if bidder and bcrypt.check_password_hash(bidder.id, form.password.data):
            login_user(bidder, remember=form.remember.data)
            return redirect(url_for('items'))
        else:
            flash('Login Unsuccessful. Please check your name and ID', 'danger')
    return render_template("login.html", title='Login', form=form)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/items")
def items():
    return render_template("items.html", items=Item.query.all())