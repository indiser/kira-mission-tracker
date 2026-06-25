/**
 * Global Authentication Interceptor
 * 
 * Ensures all API fetches include credentials (cookies) and instantly 
 * redirects to the beautiful login screen on any 401 Unauthorized response.
 * This runs before app.js, ensuring 100% compatibility with existing logic.
 */

const originalFetch = window.fetch;

window.fetch = async function(...args) {
    let [resource, config] = args;
    
    // Auto-inject credentials to allow session cookies cross-origin
    if (typeof resource === 'string' && resource.includes('/api/')) {
        config = config || {};
        config.credentials = 'include';
        args = [resource, config];
    }

    try {
        const response = await originalFetch.apply(this, args);
        
        // If unauthenticated, redirect to login page instantly
        if (response.status === 401 && window.location.pathname !== '/login') {
            window.location.href = '/login';
        }
        
        return response;
    } catch (error) {
        throw error;
    }
};

// If we are on the dashboard, proactively check authentication before rendering
if (window.location.pathname === '/') {
    fetch('/api/auth/me')
        .then(res => {
            if (res.status === 401) {
                window.location.href = '/login';
            } else if (res.ok) {
                res.json().then(user => {
                    // Update user profile in header if the elements exist
                    const userNameEl = document.getElementById('auth-username');
                    if (userNameEl) {
                        userNameEl.textContent = user.username;
                    }
                });
            }
        })
        .catch(err => console.error("Auth check failed:", err));
}

// Global logout function accessible from HTML
window.logout = function() {
    fetch('/api/auth/logout', { method: 'POST' })
        .then(() => {
            window.location.href = '/login';
        });
};
