# Generated by Django 4.0.5 on 2022-06-04 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complexprocedure',
            name='sorting',
            field=models.SmallIntegerField(blank=True, default=0, verbose_name='Номер сортировки'),
        ),
        migrations.AlterField(
            model_name='procedure',
            name='sorting',
            field=models.SmallIntegerField(blank=True, default=0, verbose_name='Номер сортировки'),
        ),
    ]
