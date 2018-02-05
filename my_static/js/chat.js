var chatSubmitAction = function(event){
    event.preventDefault();

    $.ajax({
        // url : 'messages/post/',
        type : 'POST',
        data : { content : $('#id_content').val() },

        success : function(json){
            $('#id_content').val('');
            // $('#id_msg_box').append('<li class="text-right list-group-item">' + json.content + '</li>');
            var chatThread = document.getElementById('id_msg_box');
            chatThread.scrollTop = chatThread.scrollHeight;
        }
    });
}

$('#chat-form').on('submit', chatSubmitAction);

function getMessages(){
    if (!scrolling) {
        $.get('/messages/messages', function(messages){
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
     $('#id_content').keyup(function() {
        if($(this).val() != '') {
           $('#send').removeAttr('disabled');
        }
        else {
        $('#send').attr('disabled','disabled');
        }
     });
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
