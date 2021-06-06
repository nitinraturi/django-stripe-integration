from django.db import models

# Create your models here.

class Order(models.Model):
    email = models.EmailField(max_length=254)
    paid = models.BooleanField(default="False")
    amount = models.IntegerField(default=0)
    description = models.CharField(default=None,max_length=800)
    def __str__(self):
        return self.email