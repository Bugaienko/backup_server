# Generated by Django 4.0.5 on 2022-06-10 18:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_alter_action_date_end'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='date_end',
            field=models.DateField(default=datetime.date(2022, 6, 17), verbose_name='Дата начала'),
        ),
    ]
