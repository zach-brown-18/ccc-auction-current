# Initialize database
from ccc_auction import db

db.create_all()


# Handle Items
from ccc_auction.models import Item, Bidder
from datetime import datetime
import pandas as pd

df = pd.read_csv("../database_management/auction_item_upload.txt", sep='\t', encoding='latin-1')
df = df.sort_values('Item')
df

open_time = datetime(2020, 10, 7, 8)
close_time = datetime(2020, 10, 18, 21)
image_files = [f"item_{number}.jpg" for number in df["Item"]]
for row, image in zip(df.iterrows(), image_files):
    index = row[0]
    row = row[1]
    current_bid = row['Starting Bid'] - row['Raise']

    item = Item(itemname=row['Title'], description=row['Full Description'], restrictions=row['Restrictions'], image_file=image, current_bid=current_bid, raise_value=row['Raise'], open_bid=row['Starting Bid'], list_value=row['Value'], open_time=open_time, close_time=close_time)
    db.session.add(item)

db.session.commit()


# Handle Bidders
df = pd.read_csv("../database_management/bidders.csv")
df

# Admins
bidder_zach = Bidder(id=93, biddername='ZB')
bidder_debbie = Bidder(id=60, biddername='DB')
db.session.add(bidder_zach)
db.session.add(bidder_debbie)
db.session.commit()

for idx in range(len(df)):
    bidder_id = int(df.iloc[idx]['ID'])
    name = df.iloc[idx]['User Name']
    bidder = Bidder(id=bidder_id, biddername=name)
    db.session.add(bidder)

db.session.commit()