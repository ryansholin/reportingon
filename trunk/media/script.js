$(function() {
    if ($("#search input").length) {
        $("#search input").focus(function() {
            if ($(this).attr('value') == 'Search...') {$(this).attr('value','')}
        });
        $("#search input").blur(function() {
            if ($(this).attr('value') == '') {$(this).attr('value','Search...')}
        });
    }
    if ($("#user-options").length) {
        $("#user-options").hover(
            function() {$("#user-tag").addClass('enabled');},
            function() {$("#user-tag").removeClass('enabled')}
        )
    }
});