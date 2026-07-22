const API_BASE_URL = 'http://127.0.0.1:5000/api/v1';

document.addEventListener('DOMContentLoaded', () => {
    setupLoginForm();
    setupIndexPage();
});

/**
 * Return the value of a cookie.
 *
 * @param {string} name - Name of the cookie.
 * @returns {string|null} The cookie value or null.
 */
function getCookie(name) {
    const cookiePrefix = `${name}=`;
    const cookies = document.cookie.split(';');

    for (const cookie of cookies) {
        const trimmedCookie = cookie.trim();

        if (trimmedCookie.startsWith(cookiePrefix)) {
            return decodeURIComponent(
                trimmedCookie.substring(cookiePrefix.length)
            );
        }
    }

    return null;
}

/**
 * Set up the login form from login.html.
 */
function setupLoginForm() {
    const loginForm = document.getElementById('login-form');

    if (!loginForm) {
        return;
    }

    const errorMessage = document.getElementById('login-error');
    const submitButton = loginForm.querySelector(
        'button[type="submit"]'
    );

    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const emailInput = document.getElementById('email');
        const passwordInput = document.getElementById('password');

        const email = emailInput.value.trim();
        const password = passwordInput.value;

        errorMessage.textContent = '';
        submitButton.disabled = true;
        submitButton.textContent = 'Logging in...';

        try {
            const response = await fetch(
                `${API_BASE_URL}/auth/login`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        email,
                        password
                    })
                }
            );

            let data = {};

            try {
                data = await response.json();
            } catch (error) {
                data = {};
            }

            if (!response.ok) {
                errorMessage.textContent =
                    data.error ||
                    data.message ||
                    'Invalid email or password.';
                return;
            }

            if (!data.access_token) {
                errorMessage.textContent =
                    'The server did not return an access token.';
                return;
            }

            document.cookie =
                `token=${encodeURIComponent(data.access_token)}; ` +
                'path=/; SameSite=Lax';

            window.location.href = 'index.html';
        } catch (error) {
            console.error('Login request failed:', error);

            errorMessage.textContent =
                'Unable to connect to the API. Make sure it is running.';
        } finally {
            submitButton.disabled = false;
            submitButton.textContent = 'Login';
        }
    });
}

/**
 * Set up authentication, fetching, and filtering on index.html.
 */
function setupIndexPage() {
    const placesList = document.getElementById('places-list');

    if (!placesList) {
        return;
    }

    const token = checkAuthentication();
    const priceFilter = document.getElementById('price-filter');

    priceFilter.addEventListener('change', filterPlacesByPrice);

    fetchPlaces(token);
}

/**
 * Show or hide the login link based on authentication.
 *
 * @returns {string|null} JWT token or null.
 */
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (loginLink) {
        loginLink.style.display = token ? 'none' : 'inline-block';
    }

    return token;
}

/**
 * Fetch all places from the API.
 *
 * @param {string|null} token - JWT access token.
 */
async function fetchPlaces(token) {
    const message = document.getElementById('places-message');

    try {
        const headers = {
            'Content-Type': 'application/json'
        };

        if (token) {
            headers.Authorization = `Bearer ${token}`;
        }

        const response = await fetch(
            `${API_BASE_URL}/places/`,
            {
                method: 'GET',
                headers
            }
        );

        if (!response.ok) {
            throw new Error(
                `API request failed with status ${response.status}`
            );
        }

        const data = await response.json();

        let places = [];

        if (Array.isArray(data)) {
            places = data;
        } else if (Array.isArray(data.places)) {
            places = data.places;
        }

        displayPlaces(places);
    } catch (error) {
        console.error('Unable to fetch places:', error);

        message.textContent =
            'Unable to load places. Make sure the API is running.';
        message.classList.add('error-message');
    }
}

/**
 * Display places as cards.
 *
 * @param {Array} places - Places returned by the API.
 */
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    const message = document.getElementById('places-message');

    placesList.innerHTML = '';

    if (places.length === 0) {
        message.textContent = 'No places are currently available.';
        return;
    }

    message.textContent = '';

    places.forEach((place) => {
        const card = document.createElement('article');
        const title = document.createElement('h3');
        const description = document.createElement('p');
        const location = document.createElement('p');
        const price = document.createElement('p');
        const detailsButton = document.createElement('a');

        const placeName =
            place.title ||
            place.name ||
            'Untitled Place';

        const placeDescription =
            place.description ||
            'No description is available for this place.';

        const placePrice = Number(place.price) || 0;

        card.className = 'place-card';
        card.dataset.price = String(placePrice);

        title.textContent = placeName;

        description.className = 'place-description';
        description.textContent = placeDescription;

        location.className = 'place-location';
        location.textContent = getPlaceLocation(place);

        price.className = 'price';
        price.textContent = `$${placePrice.toFixed(2)} per night`;

        detailsButton.className = 'details-button';
        detailsButton.textContent = 'View Details';
        detailsButton.href =
            `place.html?id=${encodeURIComponent(place.id || '')}`;

        card.appendChild(title);
        card.appendChild(description);
        card.appendChild(location);
        card.appendChild(price);
        card.appendChild(detailsButton);

        placesList.appendChild(card);
    });

    filterPlacesByPrice();
}

/**
 * Create readable location text from the available place data.
 *
 * @param {Object} place - A place returned by the API.
 * @returns {string} Readable location.
 */
function getPlaceLocation(place) {
    if (place.location) {
        return place.location;
    }

    if (place.city) {
        return place.city;
    }

    if (
        place.latitude !== undefined &&
        place.longitude !== undefined
    ) {
        return `Coordinates: ${place.latitude}, ${place.longitude}`;
    }

    return 'Location not provided';
}

/**
 * Filter displayed places using the selected maximum price.
 */
function filterPlacesByPrice() {
    const priceFilter = document.getElementById('price-filter');
    const placeCards = document.querySelectorAll('.place-card');

    if (!priceFilter) {
        return;
    }

    const selectedValue = priceFilter.value;

    placeCards.forEach((card) => {
        const placePrice = Number(card.dataset.price);

        if (
            selectedValue === 'all' ||
            placePrice <= Number(selectedValue)
        ) {
            card.style.display = 'flex';
        } else {
            card.style.display = 'none';
        }
    });

    updateFilterMessage();
}

/**
 * Display a message when no places match the selected price.
 */
function updateFilterMessage() {
    const message = document.getElementById('places-message');
    const placeCards = document.querySelectorAll('.place-card');

    const visibleCards = Array.from(placeCards).filter(
        (card) => card.style.display !== 'none'
    );

    if (placeCards.length > 0 && visibleCards.length === 0) {
        message.textContent =
            'No places match the selected maximum price.';
    } else if (placeCards.length > 0) {
        message.textContent = '';
    }
}
