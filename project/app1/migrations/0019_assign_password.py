# Generated by Django 5.0.6 on 2024-07-24 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0018_remove_assign_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='assign',
            name='password',
            field=models.CharField(default='Pass123', max_length=128),
        ),
    ]
