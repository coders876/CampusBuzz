# Generated by Django 2.1.4 on 2019-03-10 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_auto_20190310_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.IntegerField(blank=True, max_length=13),
        ),
    ]
