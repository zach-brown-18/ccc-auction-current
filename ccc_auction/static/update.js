$(document).ready(function() {

    $('.updateButton').on('click', function() {

        var item_id = $(this).attr('item_id');

        // Check if the bid has closed since the 'confirm bid' modal has been opened.
        if (isOpen(item_id)) {
            
            req = $.ajax({
                url : '/update',
                type : 'POST',
                data : {item_id : item_id}
            });
    
            req.done(function(data) {
    
                // If bid is successful

                var updatedMsg = "Confirm Bid on " + data.item_name + " for $" + data.next_bid;
                var updatedInstructions = 'You already hold the high bid on this item. <br><br> You may bid higher if you like!'
                var current_bid_display = "Current Bid: $" + data.current_bid;
                var next_bid_display = "Next Bid: $" + data.next_bid;
                $('#confirmBidTitle' + item_id).text(updatedMsg);
                $('#currentBidDisplay' + item_id).text(current_bid_display);
                $('#nextBidDisplay' + item_id).text(next_bid_display);
                $('#biddingInstruction' + item_id).html(updatedInstructions)
                $('#customBid' + item_id).attr({'min':data.next_bid, 'max':data.next_bid+1000, 'value':data.next_bid})
                
                // Inform the user they placed a successful bid
                generateConfirmation(item_id);


    
            });

        } else if (isEarly(item_id)) {
            earlyBidMessage(id);
        } else if (isLate(item_id)) {
            lateBidMessage(id);
        }

    });

});

function generateConfirmation(id) {
    document.getElementById("confirmationMessage" + id).innerHTML = "Bid Successful";
    document.getElementById("confirmationMessage" + id).style.display = "block";
};

function itemClosedMessage(id, time) {
    document.getElementById("openStatus" + id).innerHTML = "Bidding on this item starts " + time;
    document.getElementById("openStatus" + id).style.display = "block";
};

function earlyBidMessage(id) {
    var openTime = formatTime(id, "openTime");
    itemClosedMessage(id, openTime);
};

function lateBidMessage(id) {
    var closeTime = formatTime(id, "closeTime");
    itemClosedMessage(id, closeTime);
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