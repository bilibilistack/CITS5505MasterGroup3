// Display flashed messages as alerts if present
window.addEventListener('DOMContentLoaded', function() {
    var flashedDiv = document.getElementById('flashed-messages');
    if (flashedDiv) {
        var messages = JSON.parse(flashedDiv.getAttribute('data-messages'));
        if (Array.isArray(messages)) {
            messages.forEach(function(item) {
                // item[1] is the message text
                alert(item[1]);
            });
        }
    }
});
