from datetime import datetime
from ccc_auction import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Bidder.query.get(str(user_id))


class Bidder(db.Model, UserMixin):
    id = db.Column(db.String(4), primary_key=True) # autoincrement=True
    biddername = db.Column(db.String(30), nullable=False)
    items = db.relationship('Item', backref='current_bidder', lazy=True)   # Linked to Item class through 'bidder_id'

    def __repr__(self):
        return f"Bidder('{self.biddername}', '{self.id}')'"


class Item(db.Model):
    id = db.Column(db.String(4), primary_key=True) # autoincrement=True
    itemname = db.Column(db.String(30), nullable=False)
    grouping = db.Column(db.String(40), nullable=False)
    description = db.Column(db.String(250))
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    
    bidder_id = db.Column(db.String, db.ForeignKey('bidder.id'), nullable=False)   # Linked to Bidder class
    current_bid = db.Column(db.Integer, nullable=False)
    raise_value = db.Column(db.Integer, nullable=False)
    open_bid = db.Column(db.Integer, nullable=False) # move to ItemPreset
    list_value = db.Column(db.Integer) # move to ItemPreset


    item_background = db.relationship('ItemPreset', backref='bid_preset', lazy=True)   # Linked to ItemPreset class through 'item_id'

    def __repr__(self):
        return f"Item('{self.itemname}', '{self.grouping}', '{self.image_file}')"


class ItemPreset(db.Model):
    id = db.Column(db.String(4), primary_key=True) # autoincrement=True


    open_time = db.Column(db.DateTime, nullable=False)
    close_time = db.Column(db.DateTime, nullable=False)

    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)   # Linked to Item class

    def __repr__(self):
        return f"Item Preset('{self.open_bid}', '{self.raise_value}', '{self.list_value}', '{self.open_time}', '{self.close_time}')"