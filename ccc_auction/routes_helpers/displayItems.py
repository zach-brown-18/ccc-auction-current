from ccc_auction.models import Item

def groupItemsInColumns(cols=3):
    items = Item.query.all()
    items_split = splitItems(items, 3)
    return items_split

def splitItems(items, n_columns=3):
    split = len(items) // n_columns
    remainder = len(items) % n_columns
    if remainder > 1:
        split += 1
    i1, i2, i3 = (items[:split], items[split:2*split], items[2*split:])
    groups = (i1, i2, i3)
    return groups