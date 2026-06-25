/**
 * Login Controller
 * Handles authentication requests and UI transitions.
 */

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const errorBox = document.getElementById('login-error');
    const btnLogin = document.getElementById('btn-login');
    const btnText = btnLogin.querySelector('.btn-text');
    const btnSpinner = btnLogin.querySelector('.btn-spinner');
    
    // Password Visibility Toggle
    const togglePassword = document.getElementById('toggle-password');
    const eyeShow = document.getElementById('eye-show');
    const eyeHide = document.getElementById('eye-hide');
    
    if (togglePassword) {
        togglePassword.addEventListener('click', () => {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            if (type === 'text') {
                eyeShow.classList.add('hidden');
                eyeHide.classList.remove('hidden');
            } else {
                eyeShow.classList.remove('hidden');
                eyeHide.classList.add('hidden');
            }
            passwordInput.focus();
        });
    }

    // Auto-focus username
    setTimeout(() => usernameInput.focus(), 800);

    // Make floating label work beautifully by ensuring placeholder is empty string, 
    // css requires :not(:placeholder-shown) or :valid, so we set required attribute in HTML
    
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Hide error
        errorBox.classList.add('hidden');
        
        const username = usernameInput.value.trim();
        const password = passwordInput.value;
        
        if (!username || !password) return;
        
        // Show loading state
        btnLogin.disabled = true;
        btnText.classList.add('hidden');
        btnSpinner.classList.remove('hidden');
        
        try {
            const response = await fetch('http://localhost:8000/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password }),
                credentials: 'include' // Allow receiving and setting the secure session cookie cross-origin
            });
            
            if (response.ok) {
                // Success! Trigger cinematic exit animation
                document.querySelector('.login-glass-panel').classList.add('dashboard-transition');
                setTimeout(() => {
                    window.location.href = '/';
                }, 500);
            } else {
                // Failure
                errorBox.classList.remove('hidden');
                errorBox.textContent = 'AUTHENTICATION FAILED';
                // Reset button
                btnLogin.disabled = false;
                btnText.classList.remove('hidden');
                btnSpinner.classList.add('hidden');
                // Shake effect
                loginForm.animate([
                    { transform: 'translateX(0)' },
                    { transform: 'translateX(-10px)' },
                    { transform: 'translateX(10px)' },
                    { transform: 'translateX(-10px)' },
                    { transform: 'translateX(10px)' },
                    { transform: 'translateX(0)' }
                ], { duration: 400, easing: 'ease-in-out' });
                passwordInput.value = '';
                passwordInput.focus();
            }
        } catch (error) {
            console.error("Login request failed:", error);
            errorBox.classList.remove('hidden');
            errorBox.textContent = 'NETWORK CONNECTION FAILED';
            btnLogin.disabled = false;
            btnText.classList.remove('hidden');
            btnSpinner.classList.add('hidden');
        }
    });
});
