// List of all countries in a simple list / array from https://gist.github.com/incredimike/1469814

$(document).ready(function () {

    // Check for click events on the navbar burger icon
    $(".navbar-burger").click(function () {

        // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
        $(".navbar-burger").toggleClass("is-active");
        $(".navbar-menu").toggleClass("is-active");

    });

    // make sure conditionally shown address block is hidden on page load
     if ($('#address-has_address').is(':checked')){
        $('#address_block').show();
        console.log('address is checked, show it');
    }
    else{
        $('#address_block').hide();
        console.log('address NOT checked, hide it');
    }

    // Check for click events on has address checkbox
    $("#address-has_address").click(function () {
        //toggle on/off address entry
        $('#address_block').toggle(250);
    });

    // make sure conditionally shown review block is hidden on page load
    if ($('#review-has_review').is(':checked')){
        $('#review_block').show();
        console.log('review is checked, show it');
    }
    else{
        $('#review_block').hide();
        console.log('review NOT checked, hide it');
    }

    // Check for click has review checkbox
    $("#review-has_review").click(function () {
        //toggle on/off review entry
        $('#review_block').toggle(250);
    });

    // Check for click has event checkbox
    $("#has_event").click(function () {
        //toggle on/off revent entry
        $('#event_block').toggle(250);
    });

    // Initialize all input of type date
    var calendars = bulmaCalendar.attach('[type="datetime"]');

    // Loop on each calendar initialized
    for(var i = 0; i < calendars.length; i++) {
        // Add listener to date:selected event
        calendars[i].on('select', date => {
            console.log(date);
        });
    }

    // To access to bulmaCalendar instance of an element
    var element = document.querySelector('#event_datetime_start');
    if (element) {
        // bulmaCalendar instance is available as element.bulmaCalendar
        element.bulmaCalendar.on('select', function(datepicker) {
            console.log(datepicker.data.value());
        });
    }

    // To access to bulmaCalendar instance of an element
    var element = document.querySelector('#event_datetime_end');
    if (element) {
        // bulmaCalendar instance is available as element.bulmaCalendar
        element.bulmaCalendar.on('select', function(datepicker) {
            console.log(datepicker.data.value());
        });
    }


});
