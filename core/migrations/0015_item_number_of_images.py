# Generated by Django 3.2.5 on 2021-07-26 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20210726_0911'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='number_of_images',
            field=models.IntegerField(default=1),
        ),
    ]
