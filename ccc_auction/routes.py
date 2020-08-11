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
        # Grab the bidder's ID from the database
        bidder = Bidder.query.filter_by(biddername=form.biddername.data).first()
        # Show the 'items' page if login info is correct
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
        # Gather all items
        items = Item.query.all()

        # Build forms
        def buildForm(item):
            form = PlaceBid(prefix=item.id)
            return form
            
        def assignItem(form):
            # Give each form a unique ID to link the form to its item
            form.set_item_id(item.id)
        
        def assignGroup(form_group, form):
            form_group.append(form)

        def buildFormAssignGroup(item, form_group):
            form = buildForm(item)
            assignItem(form)
            assignGroup(form_group, form)

        # Divide into three columns
        forms1, forms2, forms3 = ([],[],[])
        third = len(items)//3
        items1, items2, items3 = (items[:third], items[third:2*third], items[2*third:])

        for item in items1:
            buildFormAssignGroup(item, forms1)

        for item in items2:
            buildFormAssignGroup(item, forms2)

        for item in items3:
            buildFormAssignGroup(item, forms3)

        # Package the items and forms together for each column
        z1, z2, z3 = (zip(items1,forms1), zip(items2,forms2), zip(items3,forms3))
        
        # To loop through all items
        forms = forms1 + forms2 + forms3
        
        return z1, z2, z3, items, forms

    z1, z2, z3, items, forms = gather_info()

    # Trigger a bid on the item and update the database upon clicking "Place Bid" button
    for form in forms:
        if form.submit.data and form.validate_on_submit():
            item = Item.query.filter(Item.id == form.item_id).first()
            item.current_bid += 99 #item.raise_value
            item.bidder_id = current_user.id
            db.session.commit()
            return redirect(url_for('items'))

    return render_template("items.html", items=items, z1=z1, z2=z2, z3=z3)