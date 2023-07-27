# Generated by Django 4.2.3 on 2023-07-26 18:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_customuser_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(max_length=14, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+9779876543210' and must be 10 digits.", regex='(\\+977)?[9]\\d{9}$'), django.core.validators.MinLengthValidator(10)]),
        ),
    ]