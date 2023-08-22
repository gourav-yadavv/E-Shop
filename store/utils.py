# The import json statement imports the built-in JSON module, which allows working with JSON data in Python.
# The from .models import * statement imports all models defined in the current app. The * is used to import all symbols from the models module.
# Import the JSON module for working with JSON data
import json

# Import models from the current app
from .models import *


# Define a function named "cookieCart" that processes the user's cart stored in cookies
# The function processes the cart information stored in cookies and constructs data structures to store cart-related information.
# A try-except block is used to handle cases where cart data might not be available in cookies.
# The items list stores individual cart items with their details.
# The order dictionary keeps track of the cart total, number of items, and whether shipping is required.
# The cartItems variable stores the count of items in the cart.
# The loop iterates through items in the cart and retrieves relevant product information.
# For each valid item, the order total, quantity, and item details are updated.
# A dictionary representing the item is added to the items list.
# If an item is not digital, the shipping flag in the order dictionary is set to True.
# The cookieCart function returns a dictionary containing the calculated cart-related data.
def cookieCart(request):
    # Initialize an empty cart dictionary if cookies do not contain cart data
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
        print('CART:', cart)
    
    # Initialize data structures to store cart-related information
    items = []  # List to store cart items
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}  # Order information
    cartItems = order['get_cart_items']  # Count of items in the cart
    
    # Iterate through items in the cart dictionary
    for i in cart:
        # Use a try block to prevent items in cart that may have been removed from causing errors
        try:
            if cart[i]['quantity'] > 0:  # Items with negative quantity are considered freebies
                cartItems += cart[i]['quantity']  # Update the count of items in the cart
                
                # Retrieve the product from the database using its ID
                product = Product.objects.get(id=i)
                total = product.price * cart[i]['quantity']  # Calculate the total cost for this item
                
                # Update order total and quantity
                order['get_cart_total'] += total
                order['get_cart_items'] += cart[i]['quantity']
                
                # Create a dictionary representing the cart item
                item = {
                    'id': product.id,
                    'product': {
                        'id': product.id,
                        'name': product.name,
                        'price': product.price,
                        'imageURL': product.imageURL
                    },
                    'quantity': cart[i]['quantity'],
                    'digital': product.digital,
                    'get_total': total,
                }
                items.append(item)  # Add the item to the list of items
                
                # Check if the item requires shipping (physical product)
                if product.digital == False:
                    order['shipping'] = True
        except:
            pass  # Ignore errors caused by missing or removed items in the cart
    
    # Return a dictionary containing cart-related data
    return {'cartItems': cartItems, 'order': order, 'items': items}


# Define a function named "cartData" that retrieves and processes cart data for the current user
# The cartData function retrieves and processes cart data for the current user, considering both authenticated and unauthenticated users.
# If the user is authenticated, the function retrieves the customer associated with the user and checks whether an order exists or needs to be created. It also retrieves items associated with the order using the related_name orderitem_set and calculates the count of items in the cart using the get_cart_items property of the order.
# If the user is not authenticated, the function uses the cookieCart function to retrieve cart data from cookies.
# The function returns a dictionary containing the calculated cart-related data, which includes the count of cart items, the order details, and the list of items in the order.
def cartData(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        customer = request.user.customer
        # Get or create an order for the authenticated customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # Retrieve items associated with the order using the related_name 'orderitem_set'
        items = order.orderitem_set.all()
        # Get the number of items in the cart using the 'get_cart_items' property of the order
        cartItems = order.get_cart_items
    else:
        # If the user is not authenticated, use the cookieCart function to retrieve cart data
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    
    # Return a dictionary containing cart-related data
    return {'cartItems': cartItems, 'order': order, 'items': items}


# Define a function named "guestOrder" that processes an order for a guest user
# The guestOrder function processes an order for a guest user who is not authenticated.
# The function extracts the guest user's name and email from the data dictionary.
# The cookieCart function is used to retrieve cart data from cookies, which contains items in the cart.
# The function either gets or creates a Customer entry in the database using the provided email. If the customer already exists, it updates the customer's name.
# An Order entry is created associated with the customer and marked as incomplete (complete=False).
# The function iterates through the items in the cart and creates OrderItem entries for each item, considering the quantity of items and whether they are freebies (negative quantity).
# Finally, the function returns the created customer and order objects.
# This function handles the process of creating an order for guest users, updating customer information, and associating products with the order items. It's a crucial part of handling orders for users who are not logged in.

def guestOrder(request, data):
    # Extract customer name and email from the data dictionary
    name = data['form']['name']
    email = data['form']['email']
    
    # Use the cookieCart function to retrieve cart data from cookies
    cookieData = cookieCart(request)
    items = cookieData['items']
    
    # Get or create a Customer entry using the provided email
    customer, created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()
    
    # Create an Order entry associated with the customer
    order = Order.objects.create(
        customer=customer,
        complete=False,
    )
    
    # Iterate through items and create OrderItem entries
    for item in items:
        product = Product.objects.get(id=item['id'])
        # Calculate quantity based on whether it's a freebie (negative quantity)
        quantity = item['quantity'] if item['quantity'] > 0 else -1 * item['quantity']
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=quantity,
        )
    
    # Return the created customer and order objects
    return customer, order
