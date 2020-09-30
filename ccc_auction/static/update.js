$(document).ready(function() {

    $('.updateButton').on('click', function() {

        var item_id = $(this).attr('item_id');
        var user_bid = Number($('#customBid' + item_id).val());

        var min_bid = Number($('#customBid' + item_id).attr('min_bid'));
        var max_bid = Number($('#customBid' + item_id).attr('max_bid'));

        // Stop and alert user if bid is not in valid range

        if (notWholeNumber(user_bid)) {

            notWholeNumberMessage(item_id);

        } else if (bidTooLow(user_bid, min_bid)) {

            bidTooLowMessage(item_id, min_bid);

        } else if (bidTooHigh(user_bid, max_bid)) {

            bidTooHighMessage(item_id, max_bid)

        } else if (isOpen(item_id)) {
            
            req = $.ajax({
                url : '/update',
                type : 'POST',
                data : {item_id : item_id, bid : user_bid}
            });
    
            req.done(function(data) {
    
                var updatedMsg = "Confirm Bid on " + data.item_name + " for $" + data.next_bid;
                var updatedInstructions = 'You already hold the high bid on this item. <br><br> You may bid higher if you like!';
                var current_bid_display = "Current Bid: $" + data.current_bid;
                var next_bid_display = "Next Bid: $" + data.next_bid;
                $('#confirmBidTitle' + item_id).text(updatedMsg);
                $('#currentBidDisplay' + item_id).text(current_bid_display);
                $('#nextBidDisplay' + item_id).text(next_bid_display);
                $('#biddingInstruction' + item_id).html(updatedInstructions);
                $('#customBid' + item_id).attr({'min_bid':data.next_bid, 'max_bid':data.next_bid+1000, 'value':data.next_bid});
                
                generateConfirmation(item_id);
    
            });

        } else if (isEarly(item_id)) {

            earlyBidMessage(item_id);

        } else if (isLate(item_id)) {

            lateBidMessage(item_id);

        }

    });

});


function notWholeNumber(user_bid) {
    if (user_bid % 1 != 0) {
        return true;
    }
    return false;
};

function bidTooLow(user_bid, min_bid) {
    if (user_bid < min_bid) {
        return true;
    }
    return false;
};

function bidTooHigh(user_bid, max_bid) {
    if (user_bid > max_bid) {
        return true;
    }
    return false;
};

function setConfirmationMsg(id, msg) {
    document.getElementById("confirmationMessage" + id).innerHTML = msg;
    document.getElementById("confirmationMessage" + id).style.display = "block";
};

function notWholeNumberMessage(id) {
    var msg = "Please bid in whole numbers only. Kindly place another bid using whole numbers!";
    setConfirmationMsg(id, msg);
};

function bidTooLowMessage(id, min_bid) {
    var msg = "The minimum bid for this item is $" + min_bid + ". Please place a bid higher than this value.";
    setConfirmationMsg(id, msg);
};

function bidTooHighMessage(id, max_bid) {
    var msg = "There is a raise limit of $1000 per bid. The maximum next bid is $" + max_bid + ". Please place multiple bids if you would like to bid higher!";
    setConfirmationMsg(id, msg);
};

function generateConfirmation(id) {
    setConfirmationMsg(id, "Bid Successful");
};

function itemClosedMessage(id, time) {
    var msg = "Bidding on this item starts " + time;
    setConfirmationMsg(id, msg)
};

function earlyBidMessage(id) {
    var openTime = formatTime(id, "openTime");
    var msg = "Bidding on this item starts " + openTime;
    setConfirmationMsg(id, msg);
};

function lateBidMessage(id) {
    var closeTime = formatTime(id, "closeTime");
    var msg = "Bidding ended " + closeTime;
    setConfirmationMsg(id, msg);
};

function formatTime(id, element_name) {
    var timePython = document.getElementById(element_name + id).innerText.trim();
    var timeString = timePython.replace(" ","T") + "-04:00";
    var jsTime = new Date(timeString);
    return jsTime;
};

function isEarly(id) {
    var today = new Date();
    openTime = formatTime(id, "openTime");

    if (today < openTime) {
        return true;
    };
    return false;
};

function isLate(id) {
    var today = new Date();
    var closeTime = formatTime(id, "closeTime");

    if (today >= closeTime) {
        return true;
    };
    return false;
};

function isOpen(id) {
    if (isEarly(id) || isLate(id)) {
        return false;
    };
    return true;
};

function isClosed(id) {
    if (isEarly(id) || isLate(id)) {
        return true;
    };
    return false;
};

function checkTimeLoadModal(id) {
    var openTime = formatTime(id, "openTime");
    var closeTime = formatTime(id, "closeTime");

    var modalID = "#confirmBid" + id;

    if (isClosed(id)) {
        $(modalID).modal('toggle')

        if (isEarly(id)) {
            earlyBidMessage(id);
        } else if (isLate(id)) {
            lateBidMessage(id);
        };
    };
};