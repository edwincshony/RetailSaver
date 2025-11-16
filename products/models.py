from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()


class Product(models.Model):
    UNIT_CHOICES = [
        ('g', 'g'),
        ('kg', 'kg'),
        ('ml', 'ml'),
        ('l', 'l'),
        ('packet', 'packet'),
    ]
    
    name = models.CharField(max_length=200)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    weight_unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='g')
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Price
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-date_added']
    
    def __str__(self):
        return f"{self.name} - {self.quantity}{self.weight_unit}"
    
    def get_weight_display(self):
        return f"{self.quantity}{self.weight_unit}"
