from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# class User(AbstractUser):
#     pass
from django.db.models import Sum


class Category(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return f'{self.name}'

InstitutionChoices = (
    ('foundation', 'foundation'),
    ('NGO', 'non governmental organisation'),
    ('local pick-up', 'local pick-up')
)

class Institution(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=516)
    type = models.CharField(choices=InstitutionChoices, default='fundacja', max_length=20)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['name']

class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=256)
    phone_number = models.CharField(max_length=12)
    city = models.CharField(max_length=126)
    zip_code = models.CharField(max_length=6)
    pick_up_date = models.DateField(blank=True, null=True)
    pick_up_time = models.TimeField(blank=True, null=True)
    pick_up_comment = models.CharField(max_length=256, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,blank=True, null=True, default=None, on_delete=models.CASCADE)

