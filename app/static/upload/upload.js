$(document).ready(function () {
    // File drop area and file input elements
    const dropArea = $('#drop-area');
    const fileInput = $('#file-input');

    // Sidebar related
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

    // hide sidebar when clicking outside of it
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

    // File drop area and file input elements

    // Prevent browser default behavior for drag and drop events
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.on(eventName, function (e) {
            e.preventDefault();
            e.stopPropagation();
        });
    });

    // Highlight the drop area when file is dragged over or hovered
    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.on(eventName, function () {
            dropArea.addClass('highlight');
        });
    });

    // Remove highlight effect when file is dragged out or dropped
    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.on(eventName, function () {
            dropArea.removeClass('highlight');
        });
    });

    // Handle file drop event
    dropArea.on('drop', function (e) {
        const dt = e.originalEvent.dataTransfer;
        const files = dt.files;

        // If files were dropped, handle these files
        if (files.length) {
            fileInput[0].files = files;
            handleFiles(files);
        }
    });

    // Handle event when files are selected by clicking the button
    fileInput.on('change', function () {
        handleFiles(this.files);
    });

    // New preview features
    function handleFiles(files) {
        if (files.length === 0) return;

        const file = files[0];
        if (file.type !== 'text/csv' && !file.name.endsWith('.csv')) {
            alert('Please upload CSV files only!');
            return;
        }

        // Display upload progress bar
        $('#upload-progress-container').show();

        // Preview CSV file
        previewCSVFile(file);

        // Post CSV file to server
        postCSVFile(file);
    }

    // Post CSV file to server
    function postCSVFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        // Reset progress bar
        const progressBar = $('#upload-progress-bar');
        const progressText = $('#upload-progress-text');
        progressBar.css('width', '0%');
        progressText.text('0%');

        // Gradually bump progress to 99% over 8 seconds
        let progress = 0;
        const interval = setInterval(() => {
            if (progress < 99) {
                progress += 1;
                progressBar.css('width', `${progress}%`);
                progressText.text(`${progress}%`);
            } else {
                clearInterval(interval);
            }
        }, 80); // 8000ms / 99 steps = ~80ms per step

        const csrfToken = $('meta[name="csrf-token"]').attr('content'); // Get CSRF token from meta tag

        $.ajax({
            url: '/upload_csv',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            headers: {
                'X-CSRFToken': csrfToken // Add CSRF token to request headers
            },
            success: function (response) {
                clearInterval(interval); // Stop gradual progress
                if (response.message && response.message.includes('uploaded and processed successfully')) {
                    // Set progress to 100% on successful response
                    progressBar.css('width', '100%');
                    progressText.text('100%');
                    alert('File uploaded successfully!');
                    console.log('Server response:', response);
                } else {
                    // Handle unexpected success responses
                    alert('Unexpected server response!');
                    console.log('Server response:', response);
                }
            },
            error: function (xhr, status, error) {
                clearInterval(interval); // Stop gradual progress
                const response = JSON.parse(xhr.responseText);
                if (xhr.status === 400) {
                    // Reset progress to 0% on error
                    progressBar.css('width', '0%');
                    progressText.text('0%');
                    const errorMessage = response.error || 'File upload failed! Please check the csv file contains all required columns and try again.';
                    alert(errorMessage);
                } else {
                    alert(response.error || 'An error occurred on server side');
                }
                console.error('Error:', error);
            }
        });
        sidebar.removeClass('collapsed');// Show sidebar after file upload automatically to let jump to other pages
    }

    // Preview CSV file
    function previewCSVFile(file) {
        const reader = new FileReader();

        reader.onload = function (e) {
            const contents = e.target.result;
            displayCSVPreview(contents);
        };

        reader.onerror = function () {
            console.error('File read error');
            $('#file-preview-container').hide();
        };

        // Start reading the file contents
        reader.readAsText(file);
    }

    // Show CSV Preview
    function displayCSVPreview(csvContent) {
        // Show preview container
        $('#file-preview-container').show();

        // Get the preview table element
        const previewTable = $('#preview-table');
        previewTable.empty();

        // Split CSV content by lines
        const rows = csvContent.split('\n');

        // Limit the number of preview rows
        const maxRows = Math.min(10, rows.length);

        for (let i = 0; i < maxRows; i++) {
            // Skip empty lines
            if (!rows[i].trim()) continue;

            const values = rows[i].split(',');

            // Creating a table row
            const tr = $('<tr></tr>');

            // Adding a table cell
            for (let value of values) {
                // The first row is the header
                if (i === 0) {
                    tr.append(`<th>${value.trim()}</th>`);
                } else {
                    tr.append(`<td>${value.trim()}</td>`);
                }
            }

            // Adding rows to a table
            previewTable.append(tr);
        }

        // Tips for adding more rows
        if (rows.length > maxRows) {
            const moreRowsMessage = $('<p></p>')
                .text(`Display the first ${maxRows - 1} rows of data, a total of ${rows.length - 1} rows.`)
                .css({
                    'text-align': 'center',
                    'padding': '10px',
                    'color': '#666',
                    'font-style': 'italic'
                });

            $('#file-preview-container').append(moreRowsMessage);
        }
    }

    const socket = io();

    $('#run-getweather-btn').on('click', function () {
        $('#getweather-progress').val('Running...\n');
        socket.emit('run_getweather');
    });

    socket.on('getweather_output', function(msg) {
        $('#getweather-progress').val(function(i, val) {
            return val + msg.data + '\n';
        });
    });
});
