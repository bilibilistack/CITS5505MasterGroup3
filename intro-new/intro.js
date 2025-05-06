document.addEventListener('DOMContentLoaded', function() {
    // Get all modules
    const modules = document.querySelectorAll('.module');
    
    // Make sure the first module is visible
    if (modules.length > 0) {
        modules[0].classList.add('visible');

        // Add click event to the first module
        modules[0].addEventListener('click', function() {
            // Remove this event listener after click to avoid repeating
            modules[0].removeEventListener('click', arguments.callee);
            
            // Show all other modules sequentially
            revealAllModules();
        });
    }

    // Function: Show all modules one by one and scroll into view
    function revealAllModules() {
        // Start from second module (index 1)
        for (let i = 1; i < modules.length; i++) {
            // Set delay for staggered display
            setTimeout(function() {
                // Show module
                modules[i].classList.add('visible');
                
                // Scroll to current module
                scrollToModule(modules[i], i);
            }, (i - 1) * 800); // 800ms interval between modules
        }
    }
    
    // Function: Smooth scroll to specified module
    function scrollToModule(module, index) {
        // Calculate module position
        const moduleRect = module.getBoundingClientRect();
        const offsetTop = moduleRect.top + window.pageYOffset;
        
        // Set scroll target position (slightly higher for better visibility)
        const scrollTarget = offsetTop - 50;
        
        // Use smooth scroll effect
        window.scrollTo({
            top: scrollTarget,
            behavior: 'smooth'
        });
    }
    
    // Picture button functionality
    const pictureBtn = document.querySelector('.picture-btn');
    if (pictureBtn) {
        // Add click event (optional)
        pictureBtn.addEventListener('click', function(e) {
            e.preventDefault(); // Prevent default anchor behavior
            
            // Placeholder for modal/fullscreen image functionality
        });
        
        // Preload image for better user experience
        const thumbnailImg = pictureBtn.querySelector('img');
        if (thumbnailImg && thumbnailImg.src) {
            const preloadImg = new Image();
            preloadImg.src = thumbnailImg.src;
        }
    }
});