# Generated by Django 4.2.6 on 2023-10-30 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_name',
            field=models.CharField(max_length=15, unique=True, verbose_name='名前'),
        ),
    ]
