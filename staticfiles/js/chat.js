var chatSubmitAction = function(event){
    event.preventDefault();

    if ($('#id_content').val().length >= 2) {
        // console.log($('#id_content').val());
        // console.log($('#id_content').val().length);
        // console.log(typeof $('#id_content').val());
        $.ajax({
            // url : 'messages/post/',
            type: 'POST',
            data: {content: $('#id_content').val()},

            success: function (json) {
                // $('#id_msg_box').append('<li class="text-right list-group-item">' + json.content + '</li>');
                $('#id_msg_box').append('' +
                    '<div class="d-flex flex-row-reverse px-2 chat_container speech-bubble_me">' +
                    '<div class="d-flex flex-column px-2">' +
                    '<div class="message-content ">' +
                    json.content +
                    '</div>' +
                    '</div>' +
                    '</div>');

                var chatThread = document.getElementById('id_msg_box');
                chatThread.scrollTop = chatThread.scrollHeight;

                $('#id_content').val('');
            }
        });
    }
};

$('#chat-form').on('submit', chatSubmitAction);

function getMessages(){
    var thread_id, pathname;
    pathname = window.location.pathname;
    thread_id = pathname.split('/')[3];

    if (!scrolling) {
        $.get('/messages/messages',{thread_id: thread_id}, function(messages){
            $('#id_msg_box').html(messages);
            var chatThread = document.getElementById('id_msg_box');
            chatThread.scrollTop = chatThread.scrollHeight;
        });
    }
    scrolling = false;
}

var scrolling = false;
$(function(){
    $('#id_msg_box').on('scroll', function(){
        scrolling = true;
    });
    refreshTimer = setInterval(getMessages, 5000);
});

$(document).ready(function() {

    $('#send').attr('disabled','disabled');
    $('#id_content').keyup(function(event) {
        if($(this).val().length > 0) {
            $('#send').removeAttr('disabled');
        } else if (event.shiftKey && event.keyCode == 13) {
            var content = this.value;
            // var caret = getCaret(this);
            //
            // console.log('content, caret');
            // console.log(content);
            // console.log(caret);
            //
            // this.value = content.substring(0, caret) + "\n" + content.substring(caret, content.length - 1);
            // event.stopPropagation();
        } else {
            $('#send').attr('disabled','disabled');
        }
    });
});

// Allow multiple line in msg_reply_box(textarea) box
$('#id_content').keyup(function (event) {
    if (event.shiftKey && event.keyCode == 13) {
        var content = this.value;
        var caret = getCaret(this);

        // console.log('content, caret');
        // console.log(content);
        // console.log(caret);

        // this.value = content.substring(0, caret) + "\n" + content.substring(caret, content.length - 1);
        this.value = content.substring(0, caret);
        event.stopPropagation();
    }
    // else if (event.keyCode == 13) {
    //     $('#chat-form').submit();
    // }
});


// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});




$("#id_content").focus(function() {
    $(this).data("hasfocus", true);
});

$("#id_content").blur(function() {
    $(this).data("hasfocus", false);
});

// TODO: This fuction repeats twice. Find way to not do this silly thing in JS.
$(document.body).keyup(function(ev) {
    // 13 is ENTER
    if (ev.which === 13 && $("#id_content").data("hasfocus")) {
        chatSubmitAction(ev)
        }
    });



// Allow multiple line in msg_reply_box(textarea) box
function getCaret(el) {
    if (el.selectionStart) {
        return el.selectionStart;
    } else if (document.selection) {
        el.focus();
        var r = document.selection.createRange();
        if (r == null) {
            return 0;
        }
        var re = el.createTextRange(),
            rc = re.duplicate();
        re.moveToBookmark(r.getBookmark());
        rc.setEndPoint('EndToStart', re);
        return rc.text.length;
    }
    return 0;
}
