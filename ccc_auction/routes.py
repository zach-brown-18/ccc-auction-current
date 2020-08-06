from ccc_auction import app, db, bcrypt
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
        if bidder and bcrypt.check_password_hash(bidder.id, form.password.data):
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
        items = Item.query.all()
        biddernames = [Bidder.query.filter(Bidder.id == item.bidder_id).first().biddername for item in items]
        third = len(items)//3

        forms1 = []
        for item in items[:third]:
            form = PlaceBid(prefix=item.id)
            form.set_item_id(item.id)
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
        
        forms = forms1 + forms2 + forms3
        z1 = zip(items[:third],biddernames[:third],forms1)
        z2 = zip(items[third:2*third],biddernames[third:2*third],forms2)
        z3 = zip(items[2*third:],biddernames[2*third:],forms3)
    
        return z1, z2, z3, items, forms

    z1, z2, z3, items, forms = gather_info()

    for form in forms:
        if form.submit.data and form.validate_on_submit():
            bidder = Bidder.query.filter_by(biddername=current_user.biddername).first()
            if bidder and bcrypt.check_password_hash(bidder.id, form.password.data):
                item = Item.query.filter(Item.id == form.item_id).first()
                item.current_bid += 99 #item.raise_value
                item.bidder_id = current_user.id
                db.session.commit()
                return redirect(url_for('items'))  
            else:
                flash('The ID you entered is incorrect. Please check your ID and try again.', 'danger')          

    return render_template("items.html", items=items, z1=z1, z2=z2, z3=z3)