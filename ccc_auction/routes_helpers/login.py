from ccc_auction.forms import LoginForm
from ccc_auction.models import Bidder

def getBidderFromLoginForm(form):
    username = form.biddername.data
    if len(username) > 2:
        case_corrected_username = username[:2].upper() + username[2:].lower()
    else:
        case_corrected_username = username.upper()
    bidder = Bidder.query.filter_by(biddername=case_corrected_username).first()
    return bidder

def biddernameMatchesId(bidder, form):
    if bidder and bidder.id == int(form.password.data):
        return True
    return False