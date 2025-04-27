$(document).ready(function() {
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
    toggleBtn.on('click', function() {
        sidebar.addClass('collapsed');
    });
    
    // Expand Sidebar
    showSidebarBtn.on('click', function() {
        sidebar.removeClass('collapsed');
    });
    
    // hide sidebar when clicking outside of it
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
    
    // Prevent browser default behavior for drag and drop events
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.on(eventName, function(e) {
            e.preventDefault();
            e.stopPropagation();
        });
    });
    
    // Highlight the drop area when file is dragged over or hovered
    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.on(eventName, function() {
            dropArea.addClass('highlight');
        });
    });
    
    // Remove highlight effect when file is dragged out or dropped
    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.on(eventName, function() {
            dropArea.removeClass('highlight');
        });
    });
    
    // Handle file drop event
    dropArea.on('drop', function(e) {
        const dt = e.originalEvent.dataTransfer;
        const files = dt.files;
        
        // If files were dropped, handle these files
        if (files.length) {
            fileInput[0].files = files;
            handleFiles(files);
        }
    });
    
    // Handle event when files are selected by clicking the button
    fileInput.on('change', function() {
        handleFiles(this.files);
    });
    
    // New preview features
    function handleFiles(files) {
        if (files.length === 0) return;
        
        const file = files[0];
        if (file.type !== 'text/csv' && !file.name.endsWith('.csv')) {
            alert('CSV files only!');
            return;
        }
        
        // Display upload progress bar
        $('#upload-progress-container').show();
        simulateFileUpload(file);
        
        // Preview CSV file
        previewCSVFile(file);
    }
    
    // Simulate file upload progress
    function simulateFileUpload(file) {
        // Reset progress bar
        const progressBar = $('#upload-progress-bar');
        const progressText = $('#upload-progress-text');
        progressBar.css('width', '0%');
        progressText.text('0%');
        
        // Initial progress value
        let progress = 0;
        
        // Simulate the upload process
        const uploadInterval = setInterval(function() {
            // Increase progress
            progress += Math.random() * 10;
            
            if (progress >= 100) {
                // Upload completed
                progress = 100;
                clearInterval(uploadInterval);
                
                // Display upload success message
                setTimeout(function() {
                    alert('upload successfully: ' + file.name);
                }, 500);
            }
            
            // Update progress bar and text
            const progressValue = Math.min(Math.round(progress), 100);
            progressBar.css('width', progressValue + '%');
            progressText.text(progressValue + '%');
        }, 100);
    }
    
    // Preview CSV file
    function previewCSVFile(file) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            const contents = e.target.result;
            displayCSVPreview(contents);
        };
        
        reader.onerror = function() {
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
                .text(`Display the first ${maxRows-1} rows of data, a total of ${rows.length-1} rows.`)
                .css({
                    'text-align': 'center',
                    'padding': '10px',
                    'color': '#666',
                    'font-style': 'italic'
                });
            
            $('#file-preview-container').append(moreRowsMessage);
        }
    }
});
