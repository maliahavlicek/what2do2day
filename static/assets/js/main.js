// List of all countries in a simple list / array from https://gist.github.com/incredimike/1469814

$(document).ready(function () {

    // Check for click events on the navbar burger icon
    $(".navbar-burger").click(function () {

        // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
        $(".navbar-burger").toggleClass("is-active");
        $(".navbar-menu").toggleClass("is-active");

    });

    // make sure conditionally shown address block is hidden on page load
    if ($('#address-has_address').is(':checked')) {
        $('#address_block').show();
        console.log('address is checked, show it');
    } else {
        $('#address_block').hide();
        console.log('address NOT checked, hide it');
    }

    // Check for click events on has address checkbox
    $("#address-has_address").click(function () {
        //toggle on/off address entry
        $('#address_block').toggle(250);
    });

    // make sure conditionally shown review block is hidden on page load
    if ($('#review-has_review').is(':checked')) {
        $('#review_block').show();
        console.log('review is checked, show it');
    } else {
        $('#review_block').hide();
        console.log('review NOT checked, hide it');
    }

    // Check for click has review checkbox
    $("#review-has_review").click(function () {
        //toggle on/off review entry
        $('#review_block').toggle(250);
    });

    // make sure conditionally shown event block is hidden on page load
    if ($('#event-has_event').is(':checked')) {
        $('#event_block').show();
        console.log('event is checked, show it');
    } else {
        $('#event_block').hide();
        console.log('event NOT checked, hide it');
    }

    // Check for click has event checkbox
    $("#event-has_event").click(function () {
        //toggle on/off revent entry
        $('#event_block').toggle(250);
    });

    // Initialize datetime
    let now = new Date();
    let today = getFormattedDate(now);
    let hour = now.getHours()+1;
    if(hour > 24){
        hour = 23;
    }
    let oneYear = getFormattedDate(new Date(now.getTime() + 24 * 60 * 60 * 1000 * 365));
    let calendars = bulmaCalendar.attach('#event-event_start_datetime', {
        isRange: true,
        labelFrom: 'Event Start',
        labelTo: 'Event End',
        minDate: today + ' ' + hour + ':00',
        maxDate: oneYear + ' ' + hour + ':00',
        minuteSteps: 15,
    });

    // Loop on each calendar initialized
    for (let i = 0; i < calendars.length; i++) {
        // Add listener to date:selected event
        calendars[i].on('select', date => {
            console.log(date);
        });
    }

    // To access to bulmaCalendar instance of an element
    let element1 = document.querySelector('#event-event_datetime_start');
    if (element1) {
        // bulmaCalendar instance is available as element.bulmaCalendar
        element1.bulmaCalendar.on('select', function (datepicker) {
            console.log(datepicker.data.value());
        });
    }


});

//from https://stackoverflow.com/questions/11591854/format-date-to-mm-dd-yyyy-in-javascript
function getFormattedDate(date) {
    let year = date.getFullYear();

    let month = (1 + date.getMonth()).toString();
    month = month.length > 1 ? month : '0' + month;

    let day = date.getDate().toString();
    day = day.length > 1 ? day : '0' + day;

    return month + '/' + day + '/' + year;
}