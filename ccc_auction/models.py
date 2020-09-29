from datetime import datetime
from ccc_auction import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Bidder.query.get(str(user_id))

class Bidder(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    biddername = db.Column(db.String(30), nullable=False)
    items = db.relationship('Item', backref='current_bidder', lazy=True)

    def __repr__(self):
        return f"Bidder('{self.biddername}', '{self.id}')'"


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    itemname = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(250))
    restrictions = db.Column(db.String(250), nullable=True)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    
    bidder_id = db.Column(db.Integer, db.ForeignKey('bidder.id'), nullable=True)
    current_bid = db.Column(db.Integer, nullable=False)
    raise_value = db.Column(db.Integer, nullable=False)
    open_bid = db.Column(db.Integer, nullable=False)
    list_value = db.Column(db.Integer)

    open_time = db.Column(db.DateTime, nullable=False)
    close_time = db.Column(db.DateTime, nullable=False)

    grouping = db.Column(db.String(40), nullable=True)

    def __repr__(self):
        return f"Item('{self.itemname}', '{self.current_bid}')"