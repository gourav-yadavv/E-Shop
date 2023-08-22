# Import the admin module from django.contrib
from django.contrib import admin

# Import all models from the current app using *
from .models import *

# Register the Customer model with the admin site
admin.site.register(Customer)

# Register the Product model with the admin site
admin.site.register(Product)

# Register the Order model with the admin site
admin.site.register(Order)

# Register the OrderItem model with the admin site
admin.site.register(OrderItem)

# Register the ShippingAddress model with the admin site
admin.site.register(ShippingAddress)


# In this code block:

# The from django.contrib import admin line imports the admin module from the django.contrib package. This module provides the tools and functionality for creating an admin interface for your app's models.

# The from .models import * line imports all models from the current app. The * is used to import all symbols from the models module.

# The admin.site.register(Customer) line registers the Customer model with the admin site. This allows you to manage customer data through the Django admin interface.

# Similarly, the admin.site.register(Product) line registers the Product model, the Order model, the OrderItem model, and the ShippingAddress model with the admin site. This enables you to manage these model instances through the admin interface as well.

# By registering the models with the admin site, you can use the admin interface to view, add, edit, and delete records for these models. It provides a user-friendly way to interact with the data stored in your app's database.