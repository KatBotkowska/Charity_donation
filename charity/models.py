from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class Category(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"


InstitutionChoices = (
    ('foundation', 'foundation'),
    ('NGO', 'non governmental organisation'),
    ('local pick-up', 'local pick-up')
)


class Institution(models.Model):
    name = models.CharField(max_length=256, verbose_name='Nazwa')
    description = models.CharField(max_length=516, verbose_name='Opis działalnosci')
    type = models.CharField(choices=InstitutionChoices, default='Fundacja', max_length=20, verbose_name='typ')
    categories = models.ManyToManyField(Category, verbose_name='Kategorie darów')

    def __str__(self):
        return f'{self.name}'

    def get_categories(self):
        return ", ".join([c.name for c in self.categories.all()])

    get_categories.short_description = 'Kategorie'

    class Meta:
        ordering = ['name']
        verbose_name = "Instytucja"
        verbose_name_plural = "Instytucje"


class Donation(models.Model):
    quantity = models.IntegerField(verbose_name='Ilość')
    categories = models.ManyToManyField(Category, verbose_name='Kategorie darów')
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, verbose_name='Instytucja')
    address = models.CharField(max_length=256, verbose_name='Adres')
    phone_number = models.CharField(max_length=12, verbose_name='Numer telefonu')
    city = models.CharField(max_length=126, verbose_name='Miasto')
    zip_code = models.CharField(max_length=6, verbose_name='Kod pocztowy')
    pick_up_date = models.DateField(blank=True, null=True, verbose_name='Data odbioru')
    pick_up_time = models.TimeField(blank=True, null=True, verbose_name='Godzina odbioru')
    pick_up_comment = models.CharField(max_length=256, blank=True, null=True, verbose_name='Dodatkowe informacje')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, default=None, on_delete=models.CASCADE,
                             verbose_name='Użytkownik')
    status = models.BooleanField(default=False, verbose_name='Czy dary odebrane?')
    update_date = models.DateField(blank=True, null=True, verbose_name='Data aktualizacji statusu', auto_now=True)

    def __str__(self):
        return f'{self.institution}'

    def get_categories(self):
        return ", ".join([c.name for c in self.categories.all()])

    get_categories.short_description = 'Kategorie'

    class Meta:
        ordering = ['status', 'pick_up_date', 'update_date']
        verbose_name = "Dary"
        verbose_name_plural = "Dary"
