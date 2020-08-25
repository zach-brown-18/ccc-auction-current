from ccc_auction.forms import LoginForm
from ccc_auction.models import Bidder

def getBidderFromLoginForm(form):
    bidder = Bidder.query.filter_by(biddername=form.biddername.data).first()
    return bidder

def biddernameMatchesId(bidder, form):
    # choose password as int or str
    if bidder and bidder.id == int(form.password.data):
        return True
    return False