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
    if ($("#new-answer-form").length) {
        $("#new-answer-form").bind("submit", function() {
            if ($("#id_comment").attr('value') == '') {
                $("#new-answer-error").css('display', 'block');
                return false;
            }
        });
    }
    if ($(".watch").length) {
        $(".watch:not(.disabled)").bind("click", function() {
            $.get($(this).attr('href'));
            return false;
        });
    }
    if ($(".rate").length) {
        $(".rate:not(.disabled)").bind("click", function() {
            $.get($(this).attr('href'));
            return false;
        });
    }
});