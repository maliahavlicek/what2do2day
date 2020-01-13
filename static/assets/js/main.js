// List of all countries in a simple list / array from https://gist.github.com/incredimike/1469814

$(document).ready(function () {

    // Check for click events on the navbar burger icon
    $(".navbar-burger").click(function () {

        // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
        $(".navbar-burger").toggleClass("is-active");
        $(".navbar-menu").toggleClass("is-active");

    });

    // Check for click events on has address checkbox
    $("#has_address").click(function () {
        //toggle on/off address entry
        $('#address_block').toggle(250);
    });

    // Check for click events on has has review checkbox
    $("#has_review").click(function () {
        //toggle on/off review entry
        $('#review_block').toggle(250);
    });
});
