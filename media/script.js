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
            $(this).addClass('loading');
            $.getJSON($(this).attr('href'), function(data) {
                var theobj = '.watch';
                $(theobj).removeClass('loading');
                if (data.status == '1') {
                    $(theobj).addClass('watched');
                } else {
                    $(theobj).removeClass('watched');
                } 
            });
            return false;
        });
    }
    if ($(".rate").length) {
        $(".rate:not(.disabled)").bind("click", function() {
            $(this).addClass('loading');
            $.getJSON($(this).attr('href'), function(data) {
                var theobj = "#rated-" + data.content_type_id + "-" + data.object_id;
                $(theobj).removeClass('loading');
                if (data.state == 'rated') {
                    $(theobj).addClass('rated-good');
                } else {
                    $(theobj).removeClass('rated-good');
                }
            });
            return false;
        });
    }
    if ($(".activity .pages").length) {
        $.each($(".activity .pages a"), function() {
            $(this).attr('href', $(this).attr('href') + '#activity')
        });
    }
});
