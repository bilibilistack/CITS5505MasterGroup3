$(document).ready(function () {
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
    const shareMessage = $('#share-message');
    const filterDate = $('#filter-date');
    const sortBy = $('#sort-by');

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
    
    const resourcesBaseUrl = "/static/chart/resources"; // Base URL for resources

    const urlParams = new URLSearchParams(window.location.search);
    const city = urlParams.get('city');
    const date = urlParams.get('date');
    const temperature_low = urlParams.get('temperature_low');
    const temperature_high = urlParams.get('temperature_high');
    const weather_description = urlParams.get('weather_description');
    const wind_speed = urlParams.get('wind_speed');
    const wind_direction = urlParams.get('wind_direction');
    const iconName = urlParams.get('icon_name') ; // Default icon name if not provided
    // Example: Display selected weather info at the top of the share page
    if (city && date) {
        const weatherInfoHtml = `
            <div class="shared-weather-info">
            <h4>Weather of ${city} </h4>
            <div class="shared-weather-info-details">
                <p>Date: ${date}</p>
                <p>Temperature: ${temperature_low}°C  ~  ${temperature_high}°C</p>
                <p>Weather: <img class="weather-icon" src="${resourcesBaseUrl}/animated_weather/${iconName}.svg" />  ${weather_description|| 'N/A'}</p>
                <p>Wind Speed: ${wind_speed ? wind_speed + ' km/h' : 'N/A'}</p>
            </div>
            </div>
        `;
        $('#weather-screenshot').html(weatherInfoHtml);
    }

    //search user
    searchBtn.click(function () {
        const searchTerm = searchInput.val();
        if (searchTerm.trim() === '') {
            userResults.empty();
            return;
        }
        // request data from database
        $.get('/search_users', { searchTerm: searchTerm }, function (data) {
            userResults.empty();
            if (data.length > 0) {
                userResults.show();
                data.forEach(function (user) {
                    const userCard = `
                <div class="user-card">
                    <div class="user-info">
                        <h4><input type="checkbox" class="user-select" data-id="${user.id}" /> ${user.username}</h4>
                    </div>
                </div>
                `;
                    userResults.append(userCard);
                });
            } else {
                userResults.append('<p>No users found.</p>');
            }
        }).fail(function () {
            userResults.empty().append('<p>Error occurred while searching. Please try again.</p>');
        });
    });

    // Trigger search on Enter key in the input field
    $('#search-user').keydown(function (e) {
        $('#search-btn').click();
    });

    // Share button click handler
    shareBtn.click(function () {
        // Get all selected users
        const selectedUsers = [];
        $('.user-select:checked').each(function () {
            selectedUsers.push($(this).data('id'));
        });

        // Get the content to share
        const contentToShare = shareMessage.val();

        // Check if any user is selected and content is provided
        if (selectedUsers.length === 0 || contentToShare.trim() === '') {
            alert('Please select at least one user and provide content to share.');
            return;
        }

        var csrfToken = $('input[name="csrf_token"]').val();

        // Prepare the data to be sent in the request body
        const dataToSend = {
            selectedUsers: selectedUsers,
            content: contentToShare,
            urlParams: {
                city: city,
                date: date,
                temperature_low: temperature_low,
                temperature_high: temperature_high,
                weather_description: weather_description,
                wind_speed: wind_speed,
                wind_direction: wind_direction,
                iconName: iconName
            }
        };

        // Send the POST request with JSON data
        $.ajax({
            url: '/share_data',
            type: 'POST',
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': csrfToken
            },
            data: JSON.stringify(dataToSend),
            success: function (response) {
                if (response.success) {
                    alert('Data shared successfully!');
                } else {
                    alert('Error sharing data.');
                }
            },
            error: function (xhr, status, error) {
                // Handle errors (e.g., server errors)
                console.error('Error sharing data:', error);
                alert('An error occurred while sharing data.');
            }
        });
    });


});
