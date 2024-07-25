# Generated by Django 5.0.6 on 2024-07-22 15:00

import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0013_alter_assign_password_alter_complaint_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assign',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$720000$5WmQpHIqTCWiA6j981qzAh$Y4bUq5sTdnce8n9CY2z3utW4nY3cJL7QvYnjltYM0AU=', max_length=128),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='Phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=13, region=None),
        ),
    ]
