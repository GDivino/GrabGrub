# Generated by Django 3.2.3 on 2021-05-29 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Kiosk', '0006_alter_food_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='created_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
