# Generated by Django 3.1.12 on 2025-01-19 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='saleorder',
            name='notes',
        ),
        migrations.AddField(
            model_name='stockmovement',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
