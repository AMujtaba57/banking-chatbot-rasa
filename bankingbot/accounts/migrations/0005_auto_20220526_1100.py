# Generated by Django 3.1.8 on 2022-05-26 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_bankuser_mobile_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankuser',
            name='mobile_number',
            field=models.TextField(),
        ),
    ]
