$(document).ready(function() {
    // Sidebar related elements
    const sidebar = $('#sidebar');
    const toggleBtn = $('#toggle-sidebar');
    const showSidebarBtn = $('#show-sidebar');
    
    // Share related elements

    const captureBtn = $('#capture-btn');
    const searchInput = $('#search-user');
    const searchBtn = $('#search-btn');
    const userResults = $('#user-results');
    const shareBtn = $('#share-btn');
    const filterDate = $('#filter-date');
    const sortBy = $('#sort-by');
    
    // Initialize the sidebar
    sidebar.addClass('collapsed');
    
    // Collapse Sidebar
    toggleBtn.on('click', function() {
        sidebar.addClass('collapsed');
    });
    
    // Expand Sidebar
    showSidebarBtn.on('click', function() {
        sidebar.removeClass('collapsed');
    });
    
    // Hide sidebar when clicking outside of it
    $(document).on('click', function(e) {
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
});
