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

$(document).ready(function() {
    // Sidebar related elements
    const sidebar = $('#sidebar');
    const toggleBtn = $('#toggle-sidebar');
    const showSidebarBtn = $('#show-sidebar');

    // Initialize the sidebar
    sidebar.addClass('collapsed');

    // Collapse Sidebar
    toggleBtn.on('click', function () {
        sidebar.addClass('collapsed');
    });

    // Expand Sidebar
    showSidebarBtn.on('click', function () {
        sidebar.removeClass('collapsed');
    });

    // Hide sidebar when clicking outside of it
    $(document).on('click', function (e) {
        if (!$(e.target).closest('#sidebar').length &&
            !$(e.target).closest('#show-sidebar').length &&
            sidebar.is(':visible') &&
            !sidebar.hasClass('collapsed')) {
            sidebar.addClass('collapsed');
        }
    });

    // Add responsive design to the sidebar
    function checkScreenSize() {
        if (window.innerWidth <= 768) {
            sidebar.addClass('collapsed');
        }
    }

    // Check screen size
    checkScreenSize();
    $(window).resize(checkScreenSize);
    
    // Initial fetch of unread count
    fetchUnreadCount();
    
    // Set interval to check for new notifications every 5 seconds
    setInterval(fetchUnreadCount, 5000);
});