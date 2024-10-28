# Generated by Django 5.1.2 on 2024-10-28 23:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='next_due_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
