# Generated by Django 3.0.5 on 2020-05-03 15:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('charity', '0005_auto_20200429_1822'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Kategoria', 'verbose_name_plural': 'Kategorie'},
        ),
        migrations.AlterModelOptions(
            name='donation',
            options={'ordering': ['institution'], 'verbose_name': 'Dary', 'verbose_name_plural': 'Dary'},
        ),
        migrations.AlterModelOptions(
            name='institution',
            options={'ordering': ['name'], 'verbose_name': 'Instytucja', 'verbose_name_plural': 'Instytucje'},
        ),
        migrations.AddField(
            model_name='donation',
            name='status',
            field=models.BooleanField(default=False, verbose_name='Czy dary odebrane?'),
        ),
        migrations.AddField(
            model_name='donation',
            name='update_date',
            field=models.DateField(auto_now=True, null=True, verbose_name='Data aktualizacji statusu'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='address',
            field=models.CharField(max_length=256, verbose_name='Adres'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='categories',
            field=models.ManyToManyField(to='charity.Category', verbose_name='Kategorie darów'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='city',
            field=models.CharField(max_length=126, verbose_name='Miasto'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='institution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='charity.Institution', verbose_name='Instytucja'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='phone_number',
            field=models.CharField(max_length=12, verbose_name='Numer telefonu'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='pick_up_comment',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Dodatkowe informacje'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='pick_up_date',
            field=models.DateField(blank=True, null=True, verbose_name='Data odbioru'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='pick_up_time',
            field=models.TimeField(blank=True, null=True, verbose_name='Godzina odbioru'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='quantity',
            field=models.IntegerField(verbose_name='Ilość'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='user',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Użytkownik'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='zip_code',
            field=models.CharField(max_length=6, verbose_name='Kod pocztowy'),
        ),
        migrations.AlterField(
            model_name='institution',
            name='categories',
            field=models.ManyToManyField(to='charity.Category', verbose_name='Kategorie darów'),
        ),
        migrations.AlterField(
            model_name='institution',
            name='description',
            field=models.CharField(max_length=516, verbose_name='Opis działalnosci'),
        ),
        migrations.AlterField(
            model_name='institution',
            name='name',
            field=models.CharField(max_length=256, verbose_name='Nazwa'),
        ),
        migrations.AlterField(
            model_name='institution',
            name='type',
            field=models.CharField(choices=[('foundation', 'foundation'), ('NGO', 'non governmental organisation'), ('local pick-up', 'local pick-up')], default='Fundacja', max_length=20, verbose_name='typ'),
        ),
    ]