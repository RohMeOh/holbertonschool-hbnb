document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const errorMessage = document.getElementById('login-error');

    if (!loginForm) {
        return;
    }

    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;
        const submitButton = loginForm.querySelector('button[type="submit"]');

        errorMessage.textContent = '';
        submitButton.disabled = true;
        submitButton.textContent = 'Logging in...';

        try {
            const response = await fetch(
                'http://127.0.0.1:5000/api/v1/auth/login',
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        email: email,
                        password: password
                    })
                }
            );

            const data = await response.json();

            if (!response.ok) {
                errorMessage.textContent =
                    data.error || data.message || 'Invalid email or password.';
                return;
            }

            if (!data.access_token) {
                errorMessage.textContent =
                    'Login succeeded, but no access token was returned.';
                return;
            }

            document.cookie =
                `token=${encodeURIComponent(data.access_token)}; path=/; SameSite=Lax`;

            window.location.href = 'index.html';
        } catch (error) {
            console.error('Login error:', error);

            errorMessage.textContent =
                'Unable to connect to the server. Make sure the API is running.';
        } finally {
            submitButton.disabled = false;
            submitButton.textContent = 'Login';
        }
    });
});
