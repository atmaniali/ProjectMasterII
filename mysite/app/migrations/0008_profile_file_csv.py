# Generated by Django 3.2.4 on 2021-06-24 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_remove_profile_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='file_csv',
            field=models.FileField(null=True, upload_to='uploads/'),
        ),
    ]