# Generated by Django 3.2.4 on 2021-06-23 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_profile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='adress',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]