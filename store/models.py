# Import the required modules from Django
from django.db import models
from django.contrib.auth.models import User


# Define the Customer model class that inherits from models.Model
# We have defined a Django model called Customer which represents a customer profile in the eCommerce system.
# The user field is a one-to-one relationship with the built-in User model from django.contrib.auth.models. It allows associating a customer profile with a user account. The on_delete=models.CASCADE specifies that if the associated user is deleted, the customer profile should be deleted as well.
# The name field is a character field used to store the customer's name. It's defined with a maximum length of 200 characters.
# The email field is another character field to store the customer's email address, also with a maximum length of 200 characters.
# The __str__ method is defined to provide a human-readable representation of the Customer object. In this case, it returns the customer's name.
class Customer(models.Model):
    # Define a one-to-one relationship with the User model.
    # A User can have one associated Customer profile and vice versa.
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    
    # Define a field to store the customer's name, with a maximum length of 200 characters.
    name = models.CharField(max_length=200, null=True)
    
    # Define a field to store the customer's email address, with a maximum length of 200 characters.
    email = models.CharField(max_length=200)
    
    # Define a human-readable string representation of the Customer object.
    def __str__(self):
        return self.name


# Define the Product model class that inherits from models.Model
# We've defined a Django model called Product which represents a product in the eCommerce system.
# The name field is a character field used to store the product's name. It's defined with a maximum length of 200 characters.
# The price field is a floating-point field to store the product's price.
# The digital field is a boolean field that defaults to False. It can be used to indicate if the product is a digital product or not. The null=True and blank=True settings allow the field to be optional.
# The image field is an ImageField that allows uploading an image for the product. It's defined with the null=True and blank=True settings to make the image field optional.
# The __str__ method is defined to provide a human-readable representation of the Product object. In this case, it returns the product's name.
# The imageURL property method is used to generate the URL of the product's image. It attempts to get the URL and handles exceptions, returning an empty string if there's an issue retrieving the URL.
class Product(models.Model):
    # Define a field to store the product's name, with a maximum length of 200 characters.
    name = models.CharField(max_length=200)
    
    # Define a field to store the product's price as a floating-point number.
    price = models.FloatField()
    
    # Define a boolean field to indicate if the product is digital (defaulting to False).
    # This might be used to differentiate between physical and digital products.
    digital = models.BooleanField(default=False, null=True, blank=True)
    
    # Define a field to store the product's image. It's an ImageField, allowing image uploads.
    image = models.ImageField(null=True, blank=True)
    
    # Define a human-readable string representation of the Product object.
    def __str__(self):
        return self.name
    
    # Define a property method to get the URL of the product's image.
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


# Define the Order model class that inherits from models.Model
#The Order class represents an order in the eCommerce system.
# The customer field is a foreign key referencing the Customer model. It uses the on_delete=models.SET_NULL option to set the customer field to NULL if the referenced customer is deleted.
# The date_ordered field stores the date and time when the order was created. The auto_now_add=True setting automatically populates it with the current datetime when an order is created.
# The complete field is a boolean field indicating whether the order is complete. It defaults to False.
# The transaction_id field stores the transaction ID associated with the order. It's a character field with a maximum length of 100 characters.
# The __str__ method returns a string representation of the order using its ID.
# The shipping property method determines if shipping is required based on whether any products in the order are not digital.
# The get_cart_total property method calculates the total cost of items in the order.
# The get_cart_items property method calculates the total number of items in the order.
class Order(models.Model):
    # Define a foreign key relationship with the Customer model.
    # If a customer is deleted, set the customer field in this order to NULL.
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Define a field to store the date and time when the order was created.
    date_ordered = models.DateTimeField(auto_now_add=True)
    
    # Define a boolean field to indicate if the order is complete.
    complete = models.BooleanField(default=False)
    
    # Define a field to store the transaction ID associated with the order.
    transaction_id = models.CharField(max_length=100, null=True)
    
    # Define a human-readable string representation of the Order object.
    def __str__(self):
        return str(self.id)
    
    # Define a property method to determine if shipping is required for the order.
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
                break
        return shipping
    
    # Define a property method to calculate the total cost of items in the cart.
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    # Define a property method to calculate the total number of items in the cart.
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

# Define the OrderItem model class that inherits from models.Model
# The OrderItem class represents an individual item within an order in the eCommerce system.
# The product field is a foreign key referencing the Product model. It uses the on_delete=models.SET_NULL option to set the product field to NULL if the referenced product is deleted.
# The order field is a foreign key referencing the Order model. It uses the on_delete=models.SET_NULL option to set the order field to NULL if the referenced order is deleted.
# The quantity field stores the quantity of the ordered product. It defaults to 0.
# The date_added field stores the date and time when the order item was added. The auto_now_add=True setting automatically populates it with the current datetime when an order item is created.
# The get_total property method calculates the total cost of the order item by multiplying the product's price with the quantity.
class OrderItem(models.Model):
    # Define a foreign key relationship with the Product model.
    # If a product is deleted, set the product field in this order item to NULL.
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    
    # Define a foreign key relationship with the Order model.
    # If an order is deleted, set the order field in this order item to NULL.
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    
    # Define a field to store the quantity of the ordered product.
    quantity = models.IntegerField(default=0, null=True, blank=True)
    
    # Define a field to store the date and time when the order item was added.
    date_added = models.DateTimeField(auto_now_add=True)
    
    # Define a property method to calculate the total cost of this order item.
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

# Define the ShippingAddress model class that inherits from models.Model
# The ShippingAddress class represents the shipping address associated with an order in the eCommerce system.
# The customer field is a foreign key referencing the Customer model. It uses the on_delete=models.SET_NULL option to set the customer field to NULL if the referenced customer is deleted.
# The order field is a foreign key referencing the Order model. It uses the on_delete=models.SET_NULL option to set the order field to NULL if the referenced order is deleted.
# The address, city, state, and zipcode fields store the components of the shipping address.
# The date_added field stores the date and time when the shipping address was added. The auto_now_add=True setting automatically populates it with the current datetime when a shipping address is created.
# The __str__ method returns a string representation of the shipping address.
class ShippingAddress(models.Model):
    # Define a foreign key relationship with the Customer model.
    # If a customer is deleted, set the customer field in this shipping address to NULL.
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    
    # Define a foreign key relationship with the Order model.
    # If an order is deleted, set the order field in this shipping address to NULL.
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    
    # Define a field to store the shipping address, with a maximum length of 200 characters.
    address = models.CharField(max_length=200, null=False)
    
    # Define a field to store the city for the shipping address, with a maximum length of 200 characters.
    city = models.CharField(max_length=200, null=False)
    
    # Define a field to store the state for the shipping address, with a maximum length of 200 characters.
    state = models.CharField(max_length=200, null=False)
    
    # Define a field to store the ZIP code for the shipping address, with a maximum length of 200 characters.
    zipcode = models.CharField(max_length=200, null=False)
    
    # Define a field to store the date and time when the shipping address was added.
    date_added = models.DateTimeField(auto_now_add=True)
    
    # Define a human-readable string representation of the ShippingAddress object.
    def __str__(self):
        return self.address