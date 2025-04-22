$(document).ready(function() {
    // File drop area and file input elements
    const dropArea = $('#drop-area');
    const fileInput = $('#file-input');
    
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
    
    // Temporary method, modified after the backend is completed
    function handleFiles(files) {
        if (files.length === 0) return;
        
        const file = files[0];
        if (file.type !== 'text/csv' && !file.name.endsWith('.csv')) {
            alert('CSV files only!');
            return;
        }
        
        alert('upload successfully: ' + file.name);
    }
});
