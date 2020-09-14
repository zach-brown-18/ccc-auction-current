from ccc_auction.forms import PlaceBid
from ccc_auction.models import Item, ItemPreset
from flask_login import current_user
from ccc_auction import db
from datetime import datetime

def gatherForms():
    items = Item.query.all()
    item_groups = splitItems(items, 3)
    form_groups = makeEmptyLists()
    buildForms(item_groups, form_groups)
    col1, col2, col3 = (zip(items, forms) for items, forms in zip(item_groups, form_groups))
    columns = [col1, col2, col3]
    all_forms = []
    for group in form_groups:
        all_forms += group
    return columns, items, all_forms

def isValidTime(form):
    item = Item.query.filter(Item.id == form.item_id).first()
    background = item.item_background[0]
    open_time = background.open_time
    close_time = background.close_time
    now = datetime.now()
    if (now >= open_time) and (now <= close_time):
        return True
    if (now < open_time):
        reason = "early"
    else:
        reason = "late"
    return (False,reason)

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

def findItemPreset(form):
    item = Item.query.filter(Item.id == form.item_id).first()
    item_preset = ItemPreset.query.filter(ItemPreset.item_id == item.id).first()
    return item_preset

def generateItemNotOpenMessage(form):
    item_preset = findItemPreset(form)
    opens = item_preset.open_time
    message = f"Bidding on this option starts {opens.month}/{opens.day}/{opens.year} at {formatDatetimeHour(opens.hour)}"
    return message

def generateItemClosedMessage(form):
    item_preset = findItemPreset(form)
    closes = item_preset.close_time
    message = f"Bidding on this option closed {closes.month}/{closes.day}/{closes.year} at {formatDatetimeHour(closes.hour)}"
    return message

def formatDatetimeHour(hour):
    if hour == 0:
        return f"12 am"
    if hour <= 11:
        return f"{hour} am"
    if hour == 12:
        return f"{hour} pm"
    return f"{hour - 12} pm"

##### gatherForms helper functions #####
def splitItems(items, n_columns=3):
    split = len(items)//n_columns
    i1, i2, i3 = (items[:split], items[split:2*split], items[2*split:])
    groups = (i1, i2, i3)
    return groups

def makeEmptyLists(n_columns=3):
    lists = [[] for col in range(n_columns)]
    return lists

def buildForms(item_groups, form_groups):
    for item_group, form_group in zip(item_groups, form_groups):
        for item in item_group:
            buildFormAssignGroup(item, form_group)

def buildFormAssignGroup(item, form_group):
    form = buildForm(item)
    assignItem(form, item)
    assignGroup(form_group, form)

def buildForm(item):
    # Prefix must be a string
    form = PlaceBid(prefix=str(item.id))
    return form

def assignItem(form, item):
    form.set_item_id(item.id)

def assignGroup(form_group, form):
    form_group.append(form)
##### End gatherForms helper functions #####