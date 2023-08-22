# Import the required modules and functions from Django
from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime

# Import the models and utility functions from the same app
from .models import * 
from .utils import cookieCart, cartData, guestOrder

# Define a view function named "store" that handles rendering the store page
# The store view function handles rendering the store page of the eCommerce website.
# The cartData function from the utils module is called to retrieve the cart data associated with the request.
# The retrieved data dictionary contains information about cart items, orders, and items in the cart.
# The cartItems variable stores the count of items in the cart.
# The order variable stores the order data.
# The items variable stores the items within the order.
# The products variable retrieves all the products from the Product model using the Product.objects.all() query.
# The context dictionary is created to pass relevant data to the template for rendering.
# The 'store/store.html' template is rendered using the render function, and the context is passed to it.
# The rendered content is returned as an HTTP response.
def store(request):
    # Call the cartData function from the utils module to retrieve cart data
    data = cartData(request)
    
    # Extract cart data from the retrieved data dictionary
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
    # Retrieve all products from the Product model
    products = Product.objects.all()
    
    # Define the context dictionary with data to be passed to the template
    context = {
        'products': products,  # List of all products
        'cartItems': cartItems,  # Number of items in the cart
    }
    
    # Render the 'store.html' template with the provided context and return the rendered content as an HTTP response
    return render(request, 'store/store.html', context)



# Define a view function named "cart" that handles rendering the cart page
# The cart view function handles rendering the cart page of the eCommerce website.
# The cartData function from the utils module is called to retrieve the cart data associated with the request.
# The retrieved data dictionary contains information about cart items, orders, and items in the cart.
# The cartItems variable stores the count of items in the cart.
# The order variable stores the order data.
# The items variable stores the items within the order.
# The context dictionary is created to pass relevant data to the template for rendering.
# The 'store/cart.html' template is rendered using the render function, and the context is passed to it.
# The rendered content is returned as an HTTP response.
def cart(request):
    # Call the cartData function from the utils module to retrieve cart data
    data = cartData(request)
    
    # Extract cart data from the retrieved data dictionary
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
    # Define the context dictionary with data to be passed to the template
    context = {
        'items': items,  # List of items in the cart
        'order': order,  # Current order data
        'cartItems': cartItems,  # Number of items in the cart
    }
    
    # Render the 'cart.html' template with the provided context and return the rendered content as an HTTP response
    return render(request, 'store/cart.html', context)


# Define a view function named "checkout" that handles rendering the checkout page
# The checkout view function handles rendering the checkout page of the eCommerce website.
# The cartData function from the utils module is called to retrieve the cart data associated with the request.
# The retrieved data dictionary contains information about cart items, orders, and items in the cart.
# The cartItems variable stores the count of items in the cart.
# The order variable stores the order data.
# The items variable stores the items within the order.
# The context dictionary is created to pass relevant data to the template for rendering.
# The 'store/checkout.html' template is rendered using the render function, and the context is passed to it.
# The rendered content is returned as an HTTP response.
def checkout(request):
    # Call the cartData function from the utils module to retrieve cart data
    data = cartData(request)
    
    # Extract cart data from the retrieved data dictionary
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
    # Define the context dictionary with data to be passed to the template
    context = {
        'items': items,  # List of items in the cart
        'order': order,  # Current order data
        'cartItems': cartItems,  # Number of items in the cart
    }
    
    # Render the 'checkout.html' template with the provided context and return the rendered content as an HTTP response
    return render(request, 'store/checkout.html', context)


# Define a view function named "updateItem" that handles updating items in the cart
# The updateItem view function handles updating the quantity of items in the cart based on the specified action (add or remove).
# JSON data is loaded from the request's body to extract the productId and action.
# Debug information is printed to the console for debugging purposes.
# The customer associated with the current user is retrieved.
# The Product model is queried to retrieve the specific product using the productId.
# An order is retrieved or created for the customer with complete=False.
# An order item associated with the order and product is retrieved or created.
# The order item's quantity is updated based on the specified action.
# The order item is saved to the database.
# If the order item's quantity becomes zero or negative, it's deleted.
# A JSON response indicating the item update is returned.
def updateItem(request):
    # Load JSON data from the request's body
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
    # Print debug information about the action and product
    print('Action:', action)
    print('Product:', productId)
    
    # Get the customer associated with the current user
    customer = request.user.customer
    
    # Retrieve the product using the productId from the Product model
    product = Product.objects.get(id=productId)
    
    # Get or create an order for the customer with complete=False
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    # Get or create an order item associated with the order and product
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    # Update the quantity of the order item based on the specified action
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    # Save the updated order item
    orderItem.save()
    
    # If the order item quantity becomes zero or negative, delete the order item
    if orderItem.quantity <= 0:
        orderItem.delete()
    
    # Return a JSON response indicating the item update
    return JsonResponse('Item was updated', safe=False)


# Define a view function named "processOrder" that handles processing customer orders
# The processOrder view function handles processing customer orders and payments.
# A unique transaction ID is generated based on the current timestamp.
# JSON data is loaded from the request's body to extract order-related information.
# If the user is authenticated, the customer and order are retrieved.
# If the user is not authenticated, the guestOrder function is used to handle the order creation.
# The total amount from the form is converted to a float.
# The transaction ID is assigned to the order.
# If the calculated total matches the order's cart total, the order is marked as complete.
# The updated order is saved to the database.
# If shipping is required (based on the order.shipping property), a new ShippingAddress entry is created.
# A JSON response indicating the payment submission is returned.
def processOrder(request):
    # Generate a unique transaction ID based on the current timestamp
    transaction_id = datetime.datetime.now().timestamp()
    
    # Load JSON data from the request's body
    data = json.loads(request.body)
    
    # If the user is authenticated, retrieve the customer and order
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        # If the user is not authenticated, use guestOrder function to handle the order
        customer, order = guestOrder(request, data)
    
    # Convert the total from the form to a float
    total = float(data['form']['total'])
    
    # Assign the transaction ID to the order
    order.transaction_id = transaction_id
    
    # If the calculated total matches the order's cart total, mark the order as complete
    if total == order.get_cart_total:
        order.complete = True
    
    # Save the updated order
    order.save()
    
    # If shipping is required, create a new ShippingAddress entry
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )
    
    # Return a JSON response indicating the payment submission
    return JsonResponse('Payment submitted..', safe=False)
