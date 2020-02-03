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
        $('#address_address_block').show();
    } else {
        $('#address_address_block').hide();
    }

    // Check for click events on has address checkbox
    $("#address-has_address").click(function () {
        //toggle on/off address entry
        $('#address_address_block').toggle(250);
    });

    // make sure conditionally shown review block is hidden on page load
    if ($('#review-has_review').is(':checked')) {
        $('#review_block').show();
    } else {
        $('#review_block').hide();
    }

    // Check for click has review checkbox
    $("#review-has_review").click(function () {
        //toggle on/off review entry
        $('#review_block').toggle(250);
    });

    // make sure conditionally shown event block is hidden on page load
    if ($('#event-has_event').is(':checked')) {
        $('#event_block').show();
    } else {
        $('#event_block').hide();
    }

    // Check for click has event checkbox
    $("#event-has_event").click(function () {
        //toggle on/off revent entry
        $('#event_block').toggle(250);
    });

    // make sure conditionally shown event address block is hidden on page load
    if ($('#event-address-has_address').is(':checked')) {
        $('#event-address_address_block').show();
    } else {
        $('#event-address_address_block').hide();
    }

    // Check for click has event checkbox
    $("#event-address-has_address").click(function () {
        //toggle on/off event address entry
        $('#event-address_address_block').toggle(250);
    });

    // Initialize datetime
    let now = new Date();
    let today = getFormattedDate(now);
    let hour = now.getHours() + 1;
    if (hour > 24) {
        hour = 23;
    }
    let tomorrow = getFormattedDate(new Date(now.getTime() + 24 * 60 * 60 * 1000));
    let oneYear = getFormattedDate(new Date(now.getTime() + 24 * 60 * 60 * 1000 * 365));
    let incomingDate = $('#event-event_start_datetime').val();


    let calendars = bulmaCalendar.attach('#event-event_start_datetime', {
        isRange: true,
        dateFormat: 'MM/DD/YYYY',
        timeFormat: 'HH:mm',
        showHeader: false,
        showTodayButton: false,
        showClearButton: false,
        validateLabel: "Select",
        minuteSteps: 15,
        labelFrom: 'Event Start',
        labelTo: 'Event End',
        minDate: today + ' ' + hour + ':00',
        maxDate: oneYear + ' ' + hour + ':00',
    });

    if (incomingDate) {
        // something wrong with bulma code and start date hours and minutes not populated
        // have a value of: MM/DD/YYYY HH:MM - MM/DD/YYYY HH:MM (startDate startTime - endDate endTime)
        // get the startDate hours and minutes
        let incomingStartHours = incomingDate.substring(11, 13);
        let incomingStartMinutes = incomingDate.substring(14, 16);
        let incomingStartDate = incomingDate.substring(0, 16);


        $('input#event-event_start_datetime').val(incomingDate);
        $('.datetimepicker-dummy-input.is-datetimepicker-range').val(incomingStartDate);
        $('.timepicker-start .timepicker-hours .timepicker-input-number').text(incomingStartHours);
        $('.datetimepicker-selection-start .datetimepicker-selection-hour').text(incomingStartHours + ':' + incomingStartMinutes);
        $('.timepicker-start .timepicker-minutes .timepicker-input-number').text(incomingStartMinutes);
    }

    // Loop on each calendar initialized
    for (let i = 0; i < calendars.length; i++) {
        // Add listener to date:selected event
        calendars[i].on('select', date => {
        });
    }

    // To access to bulmaCalendar instance of an element
    let element1 = document.querySelector('#event-event_datetime_start');
    if (element1) {
        // bulmaCalendar instance is available as element.bulmaCalendar
        element1.bulmaCalendar.on('select', function (datepicker) {
        });
    }

    /* if coming back and we have some age_limit selections, add the class */
    $('#event-age_limit option:selected').each(function () {
        let card_selector = ".card.button." + $(this).val();
        let card = $(card_selector);
        card.toggleClass('is-inverted', 10);
    });

    /* handlers for cards acting as mutli-choice selections */
    $('.card.button.ages').click(function () {
        //toggle on/off selection class and select/deselect associated selection
        $(this).toggleClass('is-inverted', 250);
        let choice_selector = $(this).attr('data-choice');
        let choice = $(choice_selector);
        let is_selected = choice.prop("selected");
        if (is_selected) {
            choice.prop("selected", false);
        } else {
            choice.prop("selected", true);
        }

    });

    /* handlers for cards acting as icon picker single-choice selections */
    $('.card.button.iconpicker').click(function () {
        //toggle on/off selection class and select/deselect associated selection
        let option = $(this);
        let is_selected = option.prop("selected");
        let input_id = $(this).data('input');
        let value_holder = $('#' + input_id);
        if (is_selected) {
            $(this).prop("selected", false);
            $(this).toggleClass('is-inverted', 250);
            value_holder.val('n')

        } else {
            //single choice so unselect the one with the inverted class, then select the current one
            $('.card.button.iconpicker.is-inverted').each(function () {
                $(this).prop("selected", false);
                $(this).toggleClass('is-inverted', 250);

            });
            let icon_file = option.data('value');
            value_holder.val(icon_file);
            option.prop("selected", true);
            option.toggleClass('is-inverted', 250);
        }
    });

    // make sure if activity_icon is something other than 'n', you preselect the right icon
    let selected_icon = $('#activity_icon').val();
    if (selected_icon !== 'n') {
        let iconpicker = $('.card.button.iconpicker[data-value="' + selected_icon + '"]');
        iconpicker.prop("selected", true);
        iconpicker.toggleClass('is-inverted', 250);
    }

    /* handlers for event-modals */
    $('.button.action.event-modal').click(function () {
        // need to pass event id to get_events to trigger modal
        let event_id = $(this).data('target');
        window.location="/get_events/"+ event_id;

    });

    /*  modals handling */
    let rootEl = document.documentElement;
    let $modals = getAll('.modal');
    /* if overlay is clicked or close button is clicked close modals */
    let $modalCloses = getAll('.modal-background, .modal-close, .modal-close-2, .delete');
    if ($modalCloses.length > 0) {
        $modalCloses.forEach(function ($el) {
            $el.addEventListener('click', function () {
                closeModals();
            });
        });
    }

    /* closing modal function */
    function closeModals() {
        rootEl.classList.remove('is-clipped');
        $modals.forEach(function ($el) {
            $el.classList.remove('is-active');
        });
    }

    /* get all from a list of selectors */
    function getAll(selector) {
        return Array.prototype.slice.call(document.querySelectorAll(selector), 0);
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

