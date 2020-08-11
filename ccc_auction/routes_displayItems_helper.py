from ccc_auction.forms import PlaceBid
from ccc_auction.models import Item
from flask_login import current_user
from ccc_auction import db

##### For displayItems function #####
##### For gatherForms function #####
def buildForm(item):
    form = PlaceBid(prefix=item.id)
    return form
    
def assignItem(form, item):
    # Give each form a unique ID to link the form to its item
    form.set_item_id(item.id)

def assignGroup(form_group, form):
    form_group.append(form)

def buildFormAssignGroup(item, form_group):
    form = buildForm(item)
    assignItem(form, item)
    assignGroup(form_group, form)

def splitItems(items, num_columns=3):
    interval = len(items)//num_columns
    items1, items2, items3 = (items[:interval], items[interval:2*interval], items[2*interval:])
    item_groups = (items1, items2, items3)
    return item_groups

def splitForms(num_columns=3):
    form_groups = [[] for col in range(num_columns)]
    return form_groups

def buildForms(item_groups, form_groups):
    for item_group, form_group in zip(item_groups, form_groups):
        for item in item_group:
            buildFormAssignGroup(item, form_group)
##### End gatherForms function #####

def gatherForms():
    items = Item.query.all()
    item_groups = splitItems(items, 3)
    form_groups = splitForms()
    buildForms(item_groups, form_groups)

    # Package the items and forms together for each column
    z1, z2, z3 = (zip(item_group, form_group) for item_group, form_group in zip(item_groups, form_groups))
    all_forms = []
    for form_group in form_groups:
        all_forms += form_group
    
    return z1, z2, z3, items, all_forms

def placeBidUpdateDatabase(form):
    item = Item.query.filter(Item.id == form.item_id).first()
    item.current_bid += 99 #item.raise_value
    item.bidder_id = current_user.id
    db.session.commit()
##### End displayItems function #####