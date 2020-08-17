from ccc_auction.forms import PlaceBid
from ccc_auction.models import Item, ItemPreset
from flask_login import current_user
from ccc_auction import db
from datetime import datetime

def gatherForms():
    items = Item.query.all()
    item_groups = splitItems(items, 3)
    form_groups = splitForms()
    buildForms(item_groups, form_groups)

    # Package the items and forms together for each column
    column1, column2, column3 = (zip(item_group, form_group) for item_group, form_group in zip(item_groups, form_groups))
    columns = [column1, column2, column3]
    all_forms = []
    for form_group in form_groups:
        all_forms += form_group
    
    return columns, items, all_forms

def isValidTime(form):
    item = Item.query.filter(Item.id == form.item_id).first()
    item_background = item.item_background[0]
    open_time = item_background.open_time
    close_time = item_background.close_time
    now = datetime.now()
    if (now >= open_time) and (now <= close_time):
        return True
    return False

def formClick(form):
    if form.submit.data and form.validate_on_submit():
        return True
    return False

def placeBidUpdateDatabase(form):
    item = Item.query.filter(Item.id == form.item_id).first()
    item.current_bid += item.raise_value
    item.bidder_id = current_user.id
    db.session.commit()

def generateConfirmationMessage(form):
    item = Item.query.filter(Item.id == form.item_id).first()
    message = f"Successfully placed bid on {item.itemname}"
    return message

##### gatherForms helper functions #####
def buildForm(item):
    form = PlaceBid(prefix=item.id)
    return form
    
def assignItem(form, item):
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
##### End gatherForms helper functions #####