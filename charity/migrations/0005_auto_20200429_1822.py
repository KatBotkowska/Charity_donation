# Generated by Django 3.0.5 on 2020-04-29 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charity', '0004_auto_20200427_1903'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='institution',
            options={'ordering': ['name']},
        ),
        migrations.AlterField(
            model_name='donation',
            name='phone_number',
            field=models.CharField(max_length=12),
        ),
        migrations.AlterField(
            model_name='donation',
            name='pick_up_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]