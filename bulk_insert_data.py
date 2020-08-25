from ccc_auction import db
from ccc_auction.models import Item, Bidder, ItemPreset
from datetime import datetime
import pandas as pd

bidder = Bidder(id=1, biddername='Zach Brown')
bidder2 = Bidder(id=2, biddername='Debbie Brown')
bidder3 = Bidder(id=3, biddername='Ye Wang')
bidder4 = Bidder(id=4, biddername='Adam Brown')
bidder5 = Bidder(id=5, biddername='Jeremy Brown')

db.session.add(bidder)
db.session.add(bidder2)
db.session.add(bidder3)
db.session.add(bidder4)
db.session.add(bidder5)

df = pd.read_csv("~/Desktop/zach/Programming/data/auction_item_upload.csv")
df

image_files = [f"item_{number}.jpg" for number in df["Item"]]

open_time = datetime(2020, 10, 7, 8)
close_time = datetime(2020, 10, 18, 21)

for row, image in zip(df.iterrows(), image_files):
    index = row[0]
    row = row[1]

    item = Item(itemname=row['Title'], description=row['Full Description'], image_file=image, current_bid=row['Starting Bid'], raise_value=row['Raise'], open_bid=row['Starting Bid'], list_value=row['Value'])
    item_preset = ItemPreset(open_time=open_time, close_time=close_time, item_id=index+1)
    
    db.session.add(item)
    db.session.add(item_preset)

db.session.commit()