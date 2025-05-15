function fetchUnreadCount() {
    $.ajax({
        url: '/unread',
        type: 'GET',
        success: function(response) {
            if (response.unread_count > 0) {
                $('#hamburger-unread').text(response.unread_count).show();
                $('#sidebar-unread').text(response.unread_count).show();
            } else {
                $('#hamburger-unread').hide();
                $('#sidebar-unread').hide();
            }
        },
        error: function() {
            console.error('Failed to fetch unread count');
        }
    });
}

/**
 * Document ready event handler
 */
$(document).ready(function() {
    // Initial fetch of unread count
    fetchUnreadCount();
    
    // Set interval to check for new notifications every 5 seconds
    setInterval(fetchUnreadCount, 5000);
});
