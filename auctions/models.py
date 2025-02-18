from django.contrib.auth.models import AbstractUser
from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator

class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=64, unique=True)
    
    def __str__(self):
        return f"{self.category}"

class Items(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_user")
    name = models.CharField(max_length=64)
    img = models.ImageField(upload_to ='uploads/')
    start_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"), validators=[MinValueValidator(Decimal("0.01"))])
    description = models.CharField(max_length=500)
    sold = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="items")
    actual_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=Decimal("0.00"))
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="owned_items", null=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.user}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField(max_length=500)
    item = models.ForeignKey(Items, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.comment}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    item = models.ForeignKey(Items, on_delete=models.CASCADE, related_name="watchlisted_by")

    def __str__(self):
        return f"{self.user} watching {self.item}"

class Bid(models.Model):
    item = models.ForeignKey(Items, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    value = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} bidded {self.value} on {self.item} at {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"