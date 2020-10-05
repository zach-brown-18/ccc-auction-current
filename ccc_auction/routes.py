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
        form_data_success, reason = biddernameMatchesId(bidder, form)
        if form_data_success:
            login_user(bidder, remember=form.remember.data)
            return redirect(url_for('displayItems'))
        elif reason == 'no bidder':
            flash('Login Unsuccessful. Please check your user name. Username is your first initial followed by your last name.', 'danger')
        elif reason == 'bidder id != form input':
            flash('Login Unsuccessful. Please check your bidder ID', 'danger')
        else:
            flash('Login Unsuccessful. Please check your user name and ID. Username is your first initial followed by your last name.', 'danger')

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
    result = 'failure'
    next_bid = item.current_bid + item.raise_value

    bid_is_current = item.current_bid == int(request.form['last_loaded_bid'])
    if bid_is_current:
        new_bid = int(request.form['bid'])
        item.current_bid = new_bid
        item.bidder_id = current_user.id
        db.session.commit()

        result = 'success'
        next_bid = new_bid + item.raise_value
    
    return {'result': result, 'item_name' : item.itemname, 'current_bid' : item.current_bid, 'next_bid' : next_bid}

@app.route("/your-items", methods=["GET"])
@login_required
def displayYourItems():
    items = current_user.items
    numbered_items = [(item, number) for item, number in zip(items, range(1, len(items)+1))]

    debbie = False
    debbie_user = Bidder.query.filter(Bidder.id == 60).first()
    if current_user == debbie_user:
        debbie = True
        items = []
        bidders = Bidder.query.all()
        for bidder in bidders:
            if bidder.items:
                for item in bidder.items:
                    bidder_username = Bidder.query.filter(Bidder.id == item.bidder_id).first().biddername
                    items.append((item, bidder_username))
        
        numbered_items = [(item, number) for item, number in zip(items, range(1, len(items)+1))]


    return render_template("current_user_items.html", items=numbered_items, debbie=debbie)