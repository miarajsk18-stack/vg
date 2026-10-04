from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    mobile = models.CharField(max_length=15)
    address = models.TextField()

class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name

    @property
    def name(self):
        return self.category_name

class Vegetable(models.Model):
    UNIT_CHOICES = (
        ('Kg', 'Kilogram'),
        ('Gram', 'Gram'),
        ('Piece', 'Piece'),
        ('Dozen', 'Dozen'),
        ('Bundle', 'Bundle'),
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='vegetables/')
    unit = models.CharField(
        max_length=20,
        choices=UNIT_CHOICES,
        default='Kg'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def category_name(self):
        return self.category.category_name if self.category else ""


class CartItem(models.Model):
	product = models.ForeignKey(Vegetable, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=0)
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.quantity} x {self.product.name}'

class Order(models.Model):
    product = models.ForeignKey(Vegetable, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    payment_status=models.CharField(max_length=255)
    payment_id=models.CharField(max_length=255)
    address=models.TextField()