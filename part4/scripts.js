const API_BASE_URL = 'http://127.0.0.1:5000/api/v1';

document.addEventListener('DOMContentLoaded', () => {
    setupLoginForm();
    setupIndexPage();
    setupPlaceDetailsPage();
});

/**
 * Return the value of a cookie.
 *
 * @param {string} name - Cookie name.
 * @returns {string|null} Cookie value or null.
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
 * Show or hide elements based on authentication.
 *
 * @returns {string|null} JWT token or null.
 */
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const addReviewSection = document.getElementById('add-review');

    if (loginLink) {
        loginLink.style.display = token ? 'none' : 'inline-block';
    }

    if (addReviewSection) {
        addReviewSection.hidden = !token;
    }

    return token;
}

/**
 * Set up the login form.
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

        const email = document
            .getElementById('email')
            .value
            .trim();

        const password = document.getElementById('password').value;

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
 * Set up the index page.
 */
function setupIndexPage() {
    const placesList = document.getElementById('places-list');

    if (!placesList) {
        return;
    }

    const token = checkAuthentication();
    const priceFilter = document.getElementById('price-filter');

    if (priceFilter) {
        priceFilter.addEventListener(
            'change',
            filterPlacesByPrice
        );
    }

    fetchPlaces(token);
}

/**
 * Fetch all places from the API.
 *
 * @param {string|null} token - JWT token.
 */
async function fetchPlaces(token) {
    const message = document.getElementById('places-message');

    try {
        const headers = {};

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
                `Unable to fetch places: ${response.status}`
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
        console.error(error);

        if (message) {
            message.textContent =
                'Unable to load places. Make sure the API is running.';
            message.classList.add('error-message');
        }
    }
}

/**
 * Display place cards on index.html.
 *
 * @param {Array} places - Places returned by the API.
 */
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    const message = document.getElementById('places-message');

    if (!placesList) {
        return;
    }

    placesList.innerHTML = '';

    if (places.length === 0) {
        if (message) {
            message.textContent =
                'No places are currently available.';
        }

        return;
    }

    if (message) {
        message.textContent = '';
    }

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
        price.textContent =
            `$${placePrice.toFixed(2)} per night`;

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
 * Return readable location information.
 *
 * @param {Object} place - Place object.
 * @returns {string} Place location.
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
 * Filter place cards by maximum price.
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
 * Show a message when no place matches the selected price.
 */
function updateFilterMessage() {
    const message = document.getElementById('places-message');
    const placeCards = document.querySelectorAll('.place-card');

    if (!message) {
        return;
    }

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

/**
 * Set up place.html.
 */
function setupPlaceDetailsPage() {
    const placeDetails = document.getElementById('place-details');

    if (!placeDetails) {
        return;
    }

    const placeId = getPlaceIdFromURL();
    const token = checkAuthentication();
    const addReviewLink = document.getElementById('add-review-link');

    if (!placeId) {
        showPlaceError('No place ID was provided in the URL.');
        return;
    }

    if (addReviewLink) {
        addReviewLink.href =
            `add_review.html?id=${encodeURIComponent(placeId)}`;
    }

    fetchPlaceDetails(token, placeId);
}

/**
 * Extract the place ID from the URL.
 *
 * Example:
 * place.html?id=123
 *
 * @returns {string|null} Place ID or null.
 */
function getPlaceIdFromURL() {
    const queryParameters = new URLSearchParams(
        window.location.search
    );

    return queryParameters.get('id');
}

/**
 * Fetch one place from the API.
 *
 * @param {string|null} token - JWT token.
 * @param {string} placeId - Place ID.
 */
async function fetchPlaceDetails(token, placeId) {
    const headers = {};

    if (token) {
        headers.Authorization = `Bearer ${token}`;
    }

    try {
        const response = await fetch(
            `${API_BASE_URL}/places/${encodeURIComponent(placeId)}`,
            {
                method: 'GET',
                headers
            }
        );

        let data = {};

        try {
            data = await response.json();
        } catch (error) {
            data = {};
        }

        if (!response.ok) {
            throw new Error(
                data.error ||
                data.message ||
                `Unable to load place: ${response.status}`
            );
        }

        const place = data.place || data;

        displayPlaceDetails(place);
    } catch (error) {
        console.error('Unable to fetch place details:', error);
        showPlaceError(error.message);
    }
}

/**
 * Display a place's complete information.
 *
 * @param {Object} place - Place returned by the API.
 */
function displayPlaceDetails(place) {
    const placeDetails = document.getElementById('place-details');
    const message = document.getElementById('place-message');

    if (!placeDetails) {
        return;
    }

    placeDetails.innerHTML = '';

    if (message) {
        message.textContent = '';
    }

    const header = document.createElement('header');
    const title = document.createElement('h1');
    const location = document.createElement('p');

    header.className = 'place-details-header';

    title.textContent =
        place.title ||
        place.name ||
        'Untitled Place';

    location.textContent = getPlaceLocation(place);

    header.appendChild(title);
    header.appendChild(location);

    const placeInfo = document.createElement('section');
    const aboutHeading = document.createElement('h2');
    const summary = document.createElement('div');
    const host = document.createElement('p');
    const price = document.createElement('p');
    const description = document.createElement('p');

    placeInfo.className = 'place-info';
    aboutHeading.textContent = 'About this place';
    summary.className = 'place-summary';

    host.textContent = `Host: ${getHostName(place)}`;
    price.textContent =
        `Price: $${(Number(place.price) || 0).toFixed(2)} per night`;

    description.className = 'place-full-description';
    description.textContent =
        place.description ||
        'No description is available for this place.';

    summary.appendChild(host);
    summary.appendChild(price);

    placeInfo.appendChild(aboutHeading);
    placeInfo.appendChild(summary);
    placeInfo.appendChild(description);
    placeInfo.appendChild(createAmenitiesSection(place.amenities));
    placeInfo.appendChild(createReviewsSection(place.reviews));

    placeDetails.appendChild(header);
    placeDetails.appendChild(placeInfo);

    document.title =
        `HBnB - ${title.textContent}`;
}

/**
 * Return the host's display name.
 *
 * @param {Object} place - Place object.
 * @returns {string} Host name.
 */
function getHostName(place) {
    const owner = place.owner || place.host;

    if (!owner) {
        return 'Not provided';
    }

    if (typeof owner === 'string') {
        return owner;
    }

    const fullName = [
        owner.first_name,
        owner.last_name
    ]
        .filter(Boolean)
        .join(' ');

    return (
        fullName ||
        owner.name ||
        owner.email ||
        'Not provided'
    );
}

/**
 * Create the amenities section.
 *
 * @param {Array} amenities - Place amenities.
 * @returns {HTMLElement} Amenities section.
 */
function createAmenitiesSection(amenities) {
    const section = document.createElement('section');
    const heading = document.createElement('h2');
    const list = document.createElement('ul');

    section.className = 'dynamic-section';
    heading.textContent = 'Amenities';
    list.className = 'amenities-list';

    if (!Array.isArray(amenities) || amenities.length === 0) {
        const item = document.createElement('li');

        item.textContent = 'No amenities listed.';
        list.appendChild(item);
    } else {
        amenities.forEach((amenity) => {
            const item = document.createElement('li');

            if (typeof amenity === 'string') {
                item.textContent = amenity;
            } else {
                item.textContent =
                    amenity.name ||
                    amenity.title ||
                    'Unnamed amenity';
            }

            list.appendChild(item);
        });
    }

    section.appendChild(heading);
    section.appendChild(list);

    return section;
}

/**
 * Create the reviews section.
 *
 * @param {Array} reviews - Place reviews.
 * @returns {HTMLElement} Reviews section.
 */
function createReviewsSection(reviews) {
    const section = document.createElement('section');
    const heading = document.createElement('h2');
    const reviewsContainer = document.createElement('div');

    section.className = 'reviews-section';
    heading.textContent = 'Guest Reviews';
    reviewsContainer.className = 'reviews-list';

    if (!Array.isArray(reviews) || reviews.length === 0) {
        const emptyMessage = document.createElement('p');

        emptyMessage.className = 'empty-state';
        emptyMessage.textContent =
            'This place does not have any reviews yet.';

        reviewsContainer.appendChild(emptyMessage);
    } else {
        reviews.forEach((review) => {
            reviewsContainer.appendChild(createReviewCard(review));
        });
    }

    section.appendChild(heading);
    section.appendChild(reviewsContainer);

    return section;
}

/**
 * Create one review card.
 *
 * @param {Object} review - Review object.
 * @returns {HTMLElement} Review card.
 */
function createReviewCard(review) {
    const card = document.createElement('article');
    const header = document.createElement('header');
    const userName = document.createElement('h3');
    const rating = document.createElement('span');
    const comment = document.createElement('p');

    card.className = 'review-card';
    header.className = 'review-card-header';
    rating.className = 'review-rating';

    userName.textContent = getReviewUserName(review);
    rating.textContent =
        `Rating: ${review.rating ?? 'Not provided'}/5`;

    comment.textContent =
        review.text ||
        review.comment ||
        review.description ||
        'No written review was provided.';

    header.appendChild(userName);
    header.appendChild(rating);

    card.appendChild(header);
    card.appendChild(comment);

    return card;
}

/**
 * Return the review author's name.
 *
 * @param {Object} review - Review object.
 * @returns {string} Review author.
 */
function getReviewUserName(review) {
    const user = review.user;

    if (!user) {
        return (
            review.user_name ||
            review.author ||
            'Anonymous Guest'
        );
    }

    if (typeof user === 'string') {
        return user;
    }

    const fullName = [
        user.first_name,
        user.last_name
    ]
        .filter(Boolean)
        .join(' ');

    return (
        fullName ||
        user.name ||
        user.email ||
        'Anonymous Guest'
    );
}

/**
 * Display an error on place.html.
 *
 * @param {string} messageText - Error message.
 */
function showPlaceError(messageText) {
    const placeDetails = document.getElementById('place-details');
    const message = document.getElementById('place-message');

    if (placeDetails) {
        placeDetails.innerHTML = '';
    }

    if (message) {
        message.textContent =
            messageText || 'Unable to load place details.';
        message.classList.add('error-message');
    }
}
