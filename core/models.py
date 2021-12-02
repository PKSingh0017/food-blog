from django.db import models
from autoslug import AutoSlugField
from django.utils import timezone
from django.contrib.auth.models import User
from django_countries.fields import CountryField

from django.shortcuts import render, get_object_or_404, redirect, reverse

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

class Carausel(models.Model):
    image= models.ImageField(upload_to='carausel_image', default='default_carausel.jpg')
    heading = models.CharField(max_length=100)
    description = models.TextField()
    button1_name = models.CharField(max_length=30, null=True, blank=True, default="Our Products")
    button1_link = models.CharField(max_length=100, null=True, blank=True, default="/#why-us")

    button2_name = models.CharField(max_length=30, null=True, blank=True, default="Our Products")
    button2_link = models.CharField(max_length=100, null=True, blank=True, default="/#why-us")
    is_active = models.BooleanField(default=False)

    def __str__(self):
        if self.is_active:
            return self.heading + ' (Active)'
        else:
            return self.heading

class Testimonial(models.Model):
    image = models.ImageField(upload_to='testimonial_image', default='default_testimonial.jpg')
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=50, null=True, blank=True)
    content = models.TextField()

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    key_ingredients = models.TextField(null=True, blank=True)

    weight = models.IntegerField(null=True, blank=True)
    allergen_information = models.CharField(max_length=100, null=True, blank=True)
    package_information = models.CharField(max_length=50, null=True, blank=True)
    diet_type = models.CharField(max_length=20, null=True, blank=True)
    package_weight = models.IntegerField(null=True, blank=True)
    nut_seed_type = models.CharField(max_length=30, null=True, blank=True)
    form = models.CharField(max_length=30, null=True, blank=True)

    price = models.IntegerField()
    discount_percentage = models.IntegerField()
    description = models.TextField()
    number_of_images = models.IntegerField(default=1)
    image1= models.ImageField(upload_to='item_pics1', default='item_default1.jpg')
    image2= models.ImageField(upload_to='item_pics2', default='item_default2.jpg')
    image3= models.ImageField(upload_to='item_pics1', default='item_default1.jpg')
    image4= models.ImageField(upload_to='item_pics2', default='item_default2.jpg')
    image5= models.ImageField(upload_to='item_pics1', default='item_default1.jpg')
    image6= models.ImageField(upload_to='item_pics2', default='item_default2.jpg')
    slug = AutoSlugField(populate_from='name', unique=True)
    

    def __str__(self):
        return self.name
    
    def actual_price(self):
        return self.price - (self.price * self.discount_percentage)/100
    
    def get_absolute_url(self):
        return reverse("product-detail", kwargs={
            'slug': self.slug
        })
    
    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={
            'slug': self.slug
        })

class OrderItem(models.Model):
    user = models.ForeignKey(User, 
    on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.name}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.get_total_item_price() - (self.quantity * self.item.discount_percentage * self.item.price / 100)

    def get_amount_saved(self):
        return self.quantity * self.item.discount_percentage * self.item.price / 100

    def get_final_price(self):
        if self.item.discount_percentage:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100, null=True)
    lastname = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    phone_number = models.CharField(max_length=15, null=True)

    rp_order_id = models.CharField(max_length=20, blank=True, null=True)
    rp_payment_id = models.CharField(max_length=20, blank=True, null=True)

    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(null=True)
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.user.username

    def is_payment_pending(self):
        if self.rp_order_id:
            if self.rp_payment_id:
                return False
            else:
                return True
        else:
            False

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total = total + order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total
    
    def get_total_quantity(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.quantity
        return total

class Address(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'

class Payment(models.Model):
    rp_payment_id = models.CharField(max_length=20, blank=True, null=True)
    rp_order_id = models.CharField(max_length=20, blank=True, null=True)
    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code

class Recipes(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    content = models.TextField()
    is_active = models.BooleanField(default=False)

    slug = AutoSlugField(populate_from='title', unique=True)

    image = models.ImageField(upload_to='recipe_images', default='default_recipe.jpg')

    def __str__(self):
        if self.is_active:
            return self.title + ' (Active)'
        else:
            return self.title
    
    def get_absolute_url(self):
        return reverse("recipe-detail", kwargs={
            'slug': self.slug
        })
    
    class Meta:
        verbose_name_plural = 'Recipes'

class Blog(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    content = models.TextField()
    is_active = models.BooleanField(default=False)

    slug = AutoSlugField(populate_from='title', unique=True)

    image = models.ImageField(upload_to='recipe_images', default='default_recipe.jpg', null=True, blank=True)

    def __str__(self):
        if self.is_active:
            return self.title + ' (Active)'
        else:
            return self.title
    
    def get_absolute_url(self):
        return reverse("blog-detail", kwargs={
            'slug': self.slug
        })

class Newsletter(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email 

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.name

class DestributionForm(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact_number = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

