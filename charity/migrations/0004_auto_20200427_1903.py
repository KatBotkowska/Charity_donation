# Generated by Django 3.0.5 on 2020-04-27 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charity', '0003_auto_20200427_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institution',
            name='type',
            field=models.CharField(choices=[('foundation', 'foundation'), ('NGO', 'non governmental organisation'), ('local pick-up', 'local pick-up')], default='fundacja', max_length=20),
        ),
    ]
