# Generated by Django 3.2.4 on 2021-06-24 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_profile_adress'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='files'),
        ),
    ]
