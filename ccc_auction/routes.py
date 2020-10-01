from ccc_auction import app, db
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user, login_required, current_user
from ccc_auction.forms import LoginForm
from ccc_auction.models import Bidder, Item
from ccc_auction.routes_helpers.displayItems import groupItemsInColumns
from ccc_auction.routes_helpers.login import getBidderFromLoginForm, biddernameMatchesId


@app.route("/", methods = ["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('displayItems'))
    form = LoginForm()
    if form.validate_on_submit():
        bidder = getBidderFromLoginForm(form)
        if biddernameMatchesId(bidder, form):        
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
    columns = groupItemsInColumns(3)
    return render_template("items.html", columns=columns, bidder=current_user)

@app.route("/update", methods=['GET','POST'])
@login_required
def updateItem():
    item = Item.query.filter(Item.id == request.form['item_id']).first()

    bid_is_current = item.current_bid == int(request.form['last_loaded_bid'])
    if bid_is_current:
        new_bid = int(request.form['bid'])
        item.current_bid = new_bid
        item.bidder_id = current_user.id
        db.session.commit()

        next_bid = new_bid + item.raise_value
        return {'result': 'success', 'item_name' : 'We Made It', 'current_bid' : item.current_bid, 'next_bid' : next_bid}
    
    next_bid = item.current_bid + item.raise_value
    return {'result': 'failure', 'item_name' : item.itemname, 'current_bid' : item.current_bid, 'next_bid' : next_bid}

@app.route("/your-items", methods=["GET"])
@login_required
def displayYourItems():
    items = current_user.items
    numbered_items = [(item, number) for item, number in zip(items, range(1, len(items)+1))]
    return render_template("current_user_items.html", items=numbered_items)