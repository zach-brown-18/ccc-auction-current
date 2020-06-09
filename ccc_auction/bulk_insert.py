from ccc_auction import db, bcrypt
from ccc_auction.models import Item, Bidder

bidder = Bidder.query.all()[0]
bidder2 = Bidder.query.all()[1]
item1 = Item(id='01', itemname='Fruit Basket', grouping='Food & Bev', description='Edible Arrangements, Perfect for gifts!', bidder_id=bidder2.id, current_bid=75)
item2 = Item(id='02', itemname='Cimarron Tequila, 1 L', grouping='Food & Bev', description='The best tequila you will ever drink! Limes not included....', bidder_id=bidder.id, current_bid=40)
item3 = Item(id='03', itemname='Joe Montana Worn Jeresy', grouping='Sports Memorabilia', description='Home jeresy from his rookie season, 1980', bidder_id=bidder.id, current_bid=650)
item4 = Item(id='04', itemname='Swimsuit', grouping='Clothing', description='Elegant Women\'s suit', bidder_id=bidder2.id, current_bid=90)
item5 = Item(id='05', itemname='Maplewood Desk', grouping='Furniture', description='For the office, home, or if your child has been extra good this year :)', bidder_id=bidder.id, current_bid=900)
item6 = Item(id='06', itemname='Example1', grouping='Example', description='Example', bidder_id=bidder.id, current_bid=75)
item7 = Item(id='07', itemname='Example2', grouping='Example', description='Example', bidder_id=bidder.id, current_bid=75)
item8 = Item(id='08', itemname='Example3', grouping='Example', description='Example', bidder_id=bidder.id, current_bid=75)
item9 = Item(id='09', itemname='Example4', grouping='Example', description='Example', bidder_id=bidder.id, current_bid=75)
item10 = Item(id='10', itemname='Example5', grouping='Example', description='Example', bidder_id=bidder.id, current_bid=75)

db.session.add(item1)
db.session.add(item2)
db.session.add(item3)
db.session.add(item4)
db.session.add(item5)
db.session.add(item6)
db.session.add(item7)
db.session.add(item8)
db.session.add(item9)
db.session.add(item10)

db.session.commit()