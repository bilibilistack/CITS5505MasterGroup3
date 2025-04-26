// Load the DOM and reflect it in the console
document.addEventListener('DOMContentLoaded', function() {
    // Initialize user data
    if (!localStorage.getItem('users')) {
        localStorage.setItem('users', JSON.stringify([]));
    }

    // Get the current page path
    const currentPath = window.location.pathname;
    
    // Login page function
    if (currentPath.includes('login.html') || currentPath === '/' || currentPath === '') {
        const loginForm = document.getElementById('loginForm');
        const errorMessage = document.getElementById('error-message');
        
        if (loginForm) {
            loginForm.addEventListener('submit', function(e) {
                e.preventDefault(); 
                
                // Getting User Input
                const username = document.getElementById('username').value;
                const password = document.getElementById('password').value;
                
                // Get user data from local storage
                const users = JSON.parse(localStorage.getItem('users'));
                
                // Authenticate User
                const user = users.find(u => u.username === username && u.password === password);
                
                if (user) {
                    // Jump to page if login is successful
                    localStorage.setItem('currentUser', username);
                    window.location.href = 'home.html';
                } else {
                    // Login failed, error message
                    errorMessage.textContent = 'Wrong username or password, please try again';
                }
            });
        }
    }
    
    // Registration page function
    if (currentPath.includes('register.html')) {
        const registerForm = document.getElementById('registerForm');
        const registerErrorMessage = document.getElementById('register-error-message');
        
        if (registerForm) {
            registerForm.addEventListener('submit', function(e) {
                e.preventDefault(); 
                
                // Getting User Input
                const newUsername = document.getElementById('newUsername').value;
                const newPassword = document.getElementById('newPassword').value;
                const confirmPassword = document.getElementById('confirmPassword').value;
                
                // Confirm that the passwords are consistent
                if (newPassword !== confirmPassword) {
                    registerErrorMessage.textContent = 'The two passwords you entered do not match. Please re-enter the password.';
                    return;
                }
                
                // Get user data from local storage
                const users = JSON.parse(localStorage.getItem('users'));
                
                // Check if the username already exists
                if (users.some(u => u.username === newUsername)) {
                    registerErrorMessage.textContent = 'This username already exists. Please use another one.';
                    return;
                }
                
                // Create a New User
                users.push({
                    username: newUsername,
                    password: newPassword
                });
                
                localStorage.setItem('users', JSON.stringify(users));
                
                // Message pop-up
                createModal('Account created successfully', function() {
                    // Jump to the login page
                    window.location.href = 'login.html';
                });
            });
        }
    }
    
    // Home page function
    if (currentPath.includes('home.html')) {
        const logoutBtn = document.getElementById('logoutBtn');
        
        // Check if the user is logged in
        const currentUser = localStorage.getItem('currentUser');
        
        if (!currentUser) {
            // If not logged in, redirect to login page
            window.location.href = 'login.html';
        }
        
        // Display the current user
        if (logoutBtn) {
            logoutBtn.addEventListener('click', function() {
                // Message pop-up
                localStorage.removeItem('currentUser');
                window.location.href = 'login.html';
            });
        }
    }
});

// Function to create a modal pop-up
function createModal(message, callback) {
    // Create modal elements
    const modal = document.createElement('div');
    modal.className = 'modal show-modal';
    
    const modalContent = document.createElement('div');
    modalContent.className = 'modal-content';
    
    const title = document.createElement('h2');
    title.textContent = message;
    
    const confirmBtn = document.createElement('button');
    confirmBtn.className = 'btn';
    confirmBtn.textContent = 'Confirm';
    
    modalContent.appendChild(title);
    modalContent.appendChild(confirmBtn);
    modal.appendChild(modalContent);
    
    // Append modal to the body
    document.body.appendChild(modal);
    
    // Add event listener to the confirm button
    confirmBtn.addEventListener('click', function() {
        // Remove modal from the DOM
        document.body.removeChild(modal);
        
        // Execute the callback function if provided
        if (typeof callback === 'function') {
            callback();
        }
    });
}
