from ast import Delete
from hashlib import blake2b
from pyexpat import model
from django.utils import timezone
from django.db import models
from django.urls import reverse

from shop.settings import AUTH_USER_MODEL

# Create your models here.

class Product (models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    price = models.FloatField(default=0.0)
    stock = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to="products", blank =True, null = True )


    def __str__(self) -> str:
        return self.name;

    def get_absolute_url(self):
        return reverse("product", kwargs={"slug": self.slug})
    
#Article (order)
"""
    -utilisateur
    -produit
    -quantite
    -commande ou non
"""
class Order(models.Model):
    #un utilisateur ->plusieur articles 
    user = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default= False)
    ordered_date = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.product.name} ({self.quantity})"

#Panier (cart)
"""
    -utilisateur
    -article
    -date commmande
    -commande ou non
"""

class Cart(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.ManyToManyField(Order)
    

    def __str__(self) -> str:
        return self.user.username

    def delete(self, *args, **kwargs):
        for order in self.order.all():
            order.ordered = True
            order.ordered_date = timezone.now()
            order.save()
        self.order.clear()
        super().delete(*args, **kwargs)
