$(document).ready(function() {
    /* Scroll on buttons */

    $('.js--scroll-to-thisdevsmind').click(function() {
        $('html, body').animate({scrollTop: $('.js--section-thisdevsmind').offset().top}, 1000);
    });

    $('.js--scroll-to-peahead').click(function() {
        $('html, body').animate({scrollTop: $('.js--section-peahead').offset().top}, 1000);
    });

    $('.js--scroll-to-danceconnect').click(function() {
        $('html, body').animate({scrollTop: $('.js--section-danceconnect').offset().top}, 1000);
    });


    /* Navigation scroll */
    $(function() {
        $('a[href*="#"]:not([href="#"], [href="#demo"])').click(function() {
            if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
                var target = $(this.hash);
                target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
                if (target.length) {
                    $('html,body').animate({
                        scrollTop: target.offset().top
                    }, 'slow');
                    return false;
                }
            }
        });
    });



    /* Notification */

    $("#notificationLink").click(function()
    {
        $("#notificationContainer").fadeToggle(300);
        $("#notification_count").fadeOut("slow");
        return false;
    });

    //Document Click hiding the popup
    $(document).click(function()
    {
        $("#notificationContainer").hide();
    });

//Popup on click
    // This stops box from closing when clicking. But also stops hrefs being clickable.
    $("#notificationContainer").click(function(event)
    {
        // event.preventDefault();
        // event.stopPropagation();

        // return false;
    });
// but Footer can be clicked
    $("#notificationFooter").click(function()
    {
        var url = window.location;
        window.location.replace(url.origin + "/profiles/notificationsbox/"); //todo temp solution
        return true;
    });
});
