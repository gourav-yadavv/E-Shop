// Get all elements with class 'update-cart'
var updateBtns = document.getElementsByClassName('update-cart');

// Loop through each 'update-cart' button
for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        // Get product ID and action from data attributes of the button
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log('productId:', productId, 'Action:', action);
        console.log('USER:', user);

        // Check if user is anonymous (not logged in)
        if (user == 'AnonymousUser') {
            addCookieItem(productId, action); // Call function to update cart using cookies
        } else {
            updateUserOrder(productId, action); // Call function to update cart for authenticated user
        }
    });
}

// Function to update cart for authenticated user
function updateUserOrder(productId, action) {
    console.log('User is authenticated, sending data...');

    // Define the URL for the update_item view
    var url = '/update_item/';

    // Use fetch to send data to the server
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken, // Cross-site request forgery token for security
        },
        body: JSON.stringify({ 'productId': productId, 'action': action }),
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        location.reload(); // Reload the page after updating the cart
    });
}

// Function to update cart using cookies for anonymous user
function addCookieItem(productId, action) {
    console.log('User is not authenticated');

    // Add or remove items from the cart stored in cookies
    if (action == 'add')
	{
        if (cart[productId] == undefined) {
            cart[productId] = { 'quantity': 1 };
        } else {
            cart[productId]['quantity'] += 1;
        }
    }

    if (action == 'remove') {
        cart[productId]['quantity'] -= 1;

        if (cart[productId]['quantity'] <= 0) {
            console.log('Item should be deleted');
            delete cart[productId];
        }
    }

    console.log('CART:', cart);

    // Update the cart cookie with the modified cart data
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";

    location.reload(); // Reload the page to reflect the changes
}
