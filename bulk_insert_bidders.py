from ccc_auction import db
from ccc_auction.models import Item, Bidder, ItemPreset
from datetime import datetime
import pandas as pd

df = pd.read_csv("../database_management/bidders.csv")
df

# Admins
# bidder_zach = Bidder(id=93, biddername='ZB')
# bidder_debbie = Bidder(id=60, biddername='DB')
# bidder_jeremy = Bidder(id=55, biddername='JB')
# db.session.add(bidder_zach)
# db.session.add(bidder_debbie)
# db.session.add(bidder_jeremy)
# db.session.commit()

for idx in range(len(df)):
    bidder_id = int(100 + df.iloc[idx]['Bidder'] - 1)
    name = df.iloc[idx]['First Name'] + ' ' + df.iloc[idx]['Last Name']
    bidder = Bidder(id=bidder_id, biddername=name)
    db.session.add(bidder)

db.session.commit()