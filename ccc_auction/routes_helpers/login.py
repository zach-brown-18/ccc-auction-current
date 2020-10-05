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
    reason = 'none'
    if bidder and bidder.id == int(form.password.data):
        return True, 'success'
    elif not bidder:
        return False, 'no bidder'
    elif bidder.id != int(form.password.data):
        return False, 'bidder id != form input'
    return False, 'none'