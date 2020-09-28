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
    
                var updatedMsg = "Confirm Bid on " + data.item_name + " for $" + data.next_bid;
                var current_bid_display = "Current Bid: $" + data.current_bid;
                var next_bid_display = "Next Bid: $" + data.next_bid;
                $('#confirmBidTitle' + item_id).text(updatedMsg);
                $('#currentBidDisplay' + item_id).text(current_bid_display);
                $('#nextBidDisplay' + item_id).text(next_bid_display);
                
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

function earlyBidMessage(id) {
    var openTime = formatOpenTime(id);
    document.getElementById("openStatus" + id).innerHTML = "Bidding on this item starts " + openTime;
    document.getElementById("openStatus" + id).style.display = "block";
};

function lateBidMessage(id) {
    var closeTime = formatCloseTime(id);
    document.getElementById("openStatus" + id).innerHTML = "Bidding on this item ended " + closeTime;
    document.getElementById("openStatus" + id).style.display = "block";
};

function formatOpenTime(id) {
    var openTimePython = document.getElementById("openTime" + id).innerText.trim();
    var openTimeString = openTimePython.replace(" ","T") + "-04:00";
    var openTime = new Date(openTimeString);
    return openTime;
};

function formatCloseTime(id) {
    var closeTimePython = document.getElementById("closeTime" + id).innerText.trim();
    var closeTimeString = closeTimePython.replace(" ","T") + "-04:00";
    var closeTime = new Date(closeTimeString);
    return closeTime;
};

function isEarly(id) {
    var today = new Date();
    openTime = formatOpenTime(id);

    if (today < openTime) {
        return true;
    };
    return false;
};

function isLate(id) {
    var today = new Date();
    closeTime = formatCloseTime(id);

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
    openTime = formatOpenTime(id);
    closeTime = formatCloseTime(id);

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

// function autoRefresh() {
//     // Refresh all items on page every 30 seconds
//     // Use jquery/ajax
//     // Issues: Removes modal from screen, Resets the page to the top

//     window.onload = setupRefresh;

//     function setupRefresh() {
//         setTimeout("refreshPage();", 10000); // milliseconds
//     };

//     function refreshPage() {
//         window.location = location.href;
//     };

// };