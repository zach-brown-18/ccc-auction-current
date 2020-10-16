from ccc_auction import db
from ccc_auction.models import Item, Bidder
import pandas as pd


df = pd.read_csv("../database_management/bidders_new.csv")
df
for idx in range(len(df)):
    bidder_id = int(df.iloc[idx]['ID'])
    name = df.iloc[idx]['User Name']
    bidder = Bidder(id=bidder_id, biddername=name)
    db.session.add(bidder)

db.session.commit()