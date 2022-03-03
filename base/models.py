from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Section(models.Model):
    name = models.CharField(max_length=300)
    def __str__(self):
        return self.name

class Drink(models.Model):
    name = models.CharField(max_length=200)
    section = models.ForeignKey(Section,on_delete=models.SET_NULL,null = True)
    description = models.TextField(null=True,blank=True)
    price = models.FloatField(blank=False,null=True)
    like = models.IntegerField(null=True,default=0)
    def __str__(self):
        return self.name

class Topping(models.Model):
    name = models.CharField(max_length=300)
    price = models.FloatField(blank=False,null=True)
    def __str__(self):
        return self.name

class Chart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    drink = models.ForeignKey(Drink,on_delete=models.SET_NULL,null = True)######todo得加一个drink
    sugar = models.TextField()
    ice = models.TextField()
    toppings = models.ManyToManyField(Topping,related_name='toppings',blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    price = models.FloatField(null=True)
    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return str(self.id)