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

    let incomingDate = false;
    let date_val = false;
    let cal_selector = false;
    let cal_start = today;
    if ($('#event-event_start_datetime').length > 0) {
        cal_selector = '#event-event_start_datetime';
        incomingDate = $(cal_selector);
        date_val = incomingDate.val();
        let incomingStartDate = date_val.substring(0, 16);
        if (incomingStartDate !== "" && incomingStartDate < today) {
            cal_start = incomingStartDate;
        }
    } else if ($('#event_start_datetime').length > 0) {
        cal_selector = '#event_start_datetime';
        incomingDate = $(cal_selector);
        if (incomingDate.length > 0) {
            date_val = incomingDate.val();
        }

        let incomingStartDate = date_val.substring(0, 16);
        if (incomingStartDate !== "" && incomingStartDate < today) {
            cal_start = incomingStartDate;
        }
    }

    if (cal_selector) {

        let calendars = bulmaCalendar.attach(cal_selector, {
            typ: 'datetime',
            isRange: true,
            dateFormat: 'MM/DD/YYYY',
            showHeader: false,
            showTodayButton: false,
            showClearButton: false,
            validateLabel: "Select",
            minuteSteps: 15,
            labelFrom: 'Start',
            labelTo: 'End',
            minDate: cal_start,
            maxDate: oneYear,
        });

        if (incomingDate) {
            // something wrong with bulma code and start date hours and minutes not populated
            // have a value of: MM/DD/YYYY HH:MM - MM/DD/YYYY HH:MM (startDate startTime - endDate endTime)
            // get the startDate hours and minutes

            if(date_val !=="") {
                incomingDate.val(date_val);

                let incomingStartHours = date_val.substring(11, 13);
                let incomingStartMinutes = date_val.substring(14, 16);
                let incomingStartDate = date_val.substring(0, 16);
                $('.datetimepicker-dummy-input.is-datetimepicker-range').val(incomingStartDate);
                $('.timepicker-start .timepicker-hours .timepicker-input-number').text(incomingStartHours);
                $('.datetimepicker-selection-start .datetimepicker-selection-hour').text(incomingStartHours + ':' + incomingStartMinutes);
                $('.timepicker-start .timepicker-minutes .timepicker-input-number').text(incomingStartMinutes);
            }
        }

        // Loop on each calendar initialized
        for (let i = 0; i < calendars.length; i++) {
            // Add listener to date:selected event
            calendars[i].on('select', date => {
            });
        }

        // To access to bulmaCalendar instance of an element
        let element1 = document.querySelector(cal_selector);
        if (element1) {
            // bulmaCalendar instance is available as element.bulmaCalendar
            element1.bulmaCalendar.on('select', function (datepicker) {
            });
        }
    }

    /* filtering results by date */
    let date_range_filter = $('#filter_date_range');
    let filterDate = date_range_filter.val();

    let filter_cal = bulmaCalendar.attach('#filter_date_range', {
        type: 'date',
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
        minDate: today,
        maxDate: oneYear,
    });

    if (filterDate) {
        // something wrong with bulma code and start date hours and minutes not populated
        // have a value of: MM/DD/YYYY HH:MM - MM/DD/YYYY HH:MM (startDate startTime - endDate endTime)
        // get the startDate hours and minutes
        let incomingStartDate = filterDate.substring(0, 10);
        $('input#filter_date_range').val(filterDate);
        $('.datetimepicker-dummy-input.is-datetimepicker-range').val(incomingStartDate);

    }
// Loop on each calendar initialized
    for (let i = 0; i < filter_cal.length; i++) {
        // Add listener to date:selected event
        filter_cal[i].on('select', date => {
        });
    }

    // To access to bulmaCalendar instance of an element
    let element2 = document.querySelector('#filter_date_range');
    if (element2) {
        // bulmaCalendar instance is available as element.bulmaCalendar
        element2.bulmaCalendar.on('select', function (datepicker) {
        });
    }


    /* if coming back and we have some activity selections, add the class */
    $('#activity option:selected').each(function () {
        let card_selector = ".card.button." + $(this).val();
        let card = $(card_selector);
        card.toggleClass('is-inverted', 10);
    });


    /* if coming back and we have some age_limit selections, add the class */
    $('#event-age_limit option:selected').each(function () {
        let card_selector = ".card.button." + $(this).val();
        let card = $(card_selector);
        card.toggleClass('is-inverted', 10);
    });

    /* if coming back and we have some age_limit selections, add the class */
    $('#age_limit option:selected').each(function () {
        let card_selector = ".card.button." + $(this).val();
        let card = $(card_selector);
        card.toggleClass('is-inverted', 10);
    });


    /* if coming back, pre-select selections */
    if ($('#activity_selection').length > 0) {
        let filter_activity_selection = $('#activity_selection').val().split("~");
        for (let i = 0; i < filter_activity_selection.length; i++) {
            if (filter_activity_selection[i] !== "n") {
                let card_selector = '.card.button.activities[data-choice="' + filter_activity_selection[i] + '"]';
                let card = $(card_selector);
                card.toggleClass('is-inverted', 10);
            }
        }
    }


    /* handlers for cards acting as mutli-choice selections */
    $('.card.button.activities').click(function () {
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

        /* save off selections in hidden field */
        let val_selections = "n";
        $('.card.button.activities.is-inverted').each(function () {
            val_selections += "~" + ($(this).attr('data-choice'));
        });

        $('#activity_selection').val(val_selections);
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
    $('.button.action.event-modal').not('.is-disabled').click(function () {
        // need to pass event id to get_events to trigger modal
        let event_id = $(this).data('target');
        window.location = "/get_events/" + event_id;

    });

    /* handlers for place add review buttons */
    $('.button.action.review-add').click(function () {
        // need to pass place id to add_review
        let place_id = $(this).data('target');
        window.location = "/add_review/" + place_id;
    });

    /* handlers for place add event buttons */
    $('.button.action.event-add').click(function () {
        // need to pass place id to add_review
        let place_id = $(this).data('target');
        window.location = "/new_event/" + place_id;
    });

     /* handlers for place add event buttons */
    $('.button.action.place-edit').click(function () {
        // need to pass place id to add_review
        let place_id = $(this).data('target');
        window.location = "/update_place/" + place_id;
    });


    /*  modals handling */
    let rootEl = document.documentElement;
    let $modals = getAll('.modal');
    /* if overlay is clicked or close button is clicked close modals */
    let $modalCloses = getAll('.modal-background, .modal-close, .modal-close-2, .delete');
    if ($modalCloses.length > 0) {
        $modalCloses.forEach(function ($el) {
            $el.addEventListener('click', function () {
                let target = $(this).parents('.modal').data('target');
                if (typeof target !== "undefined") {
                    window.location = target;
                }
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

    /* accordions */
    let accordions = bulmaAccordion.attach();

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


/* MAYbe try this to scroll activity selection into view from https://stackoverflow.com/questions/635706/how-to-scroll-to-an-element-inside-a-div */
