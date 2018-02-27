var updateSuccess = function (response) {
    var notification_box = $(nfBoxListClassSelector);
    var notifications = response.notifications;
    notifications = notifications.reverse(); //need so it's arranged by latest date

    // console.log('===UpdateSuccess===');
    // console.log(notification_box);

    // console.log(response);
    // console.log(notifications);

    notification_box.empty(); // To clear notification so it doesn't always get bigger and bigger
    $.each(notifications, function (i, notification) {
        notification_box.prepend(notification.html);
    });
};
