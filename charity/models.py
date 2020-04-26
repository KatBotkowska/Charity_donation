from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# class User(AbstractUser):
#     pass

class Category(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return f'{self.name}'

InstitutionChoices = (
    ('fundacja', 'fundacja'),
    ('NGO', 'organizacja pozarządowa'),
    ('zbiórka lokalna', 'zbiórka lokalna')
)

class Institution(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=516)
    type = models.CharField(choices=InstitutionChoices, default='fundacja', max_length=20)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return f'{self.name}'

class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=256)
    phone_number = models.IntegerField()
    city = models.CharField(max_length=126)
    zip_code = models.CharField(max_length=6)
    pick_up_date = models.DateField()
    pick_up_time = models.CharField(max_length=56)
    pick_up_comment = models.CharField(max_length=256)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,blank=True, null=True, default=None, on_delete=models.CASCADE)