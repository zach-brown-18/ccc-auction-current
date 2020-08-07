from ccc_auction import app, db
from flask import render_template, url_for, flash, redirect
from ccc_auction.forms import LoginForm, PlaceBid
from ccc_auction.models import Bidder, Item
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/", methods = ["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('items'))
    form = LoginForm()
    if form.validate_on_submit():
        bidder = Bidder.query.filter_by(biddername=form.biddername.data).first()
        # NEW - Bypassing bcrypt
        if bidder and bidder.id == form.password.data:
            login_user(bidder, remember=form.remember.data)
            return redirect(url_for('items'))
        else:
            flash('Login Unsuccessful. Please check your name and ID', 'danger')
            
    return render_template("login.html", title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('items'))

@app.route("/items", methods=['GET', 'POST'])
@login_required
def items():
    def gather_info():
        # Gather all items and bidders
        items = Item.query.all()
        biddernames = [Bidder.query.filter(Bidder.id == item.bidder_id).first().biddername for item in items]
        third = len(items)//3 # Split by the number of columns

        # Build forms
        forms1 = []
        for item in items[:third]:
            form = PlaceBid(prefix=item.id)
            form.set_item_id(item.id) # Give each form a unique ID to link it to its item
            forms1.append(form)
        
        forms2 = []
        for item in items[third:2*third]:
            form = PlaceBid(prefix=item.id)
            form.set_item_id(item.id)
            forms2.append(form)
        
        forms3 = []
        for item in items[2*third:]:
            form = PlaceBid(prefix=item.id)
            form.set_item_id(item.id)
            forms3.append(form)
        
        # Package the items, biddernames (soon to be IDs), and forms together for each column
        z1 = zip(items[:third],biddernames[:third],forms1)
        z2 = zip(items[third:2*third],biddernames[third:2*third],forms2)
        z3 = zip(items[2*third:],biddernames[2*third:],forms3)

        forms = forms1 + forms2 + forms2
        
        return z1, z2, z3, items, forms

    z1, z2, z3, items, forms = gather_info()

    # Trigger a bid on the item and update the database upon clicking "Place Bid" button
    for form in forms:
        if form.submit.data and form.validate_on_submit():
            bidder = Bidder.query.filter_by(biddername=current_user.biddername).first()
            item = Item.query.filter(Item.id == form.item_id).first()
            item.current_bid += 99 #item.raise_value
            item.bidder_id = current_user.id
            db.session.commit()
            return redirect(url_for('items'))

    return render_template("items.html", items=items, z1=z1, z2=z2, z3=z3)