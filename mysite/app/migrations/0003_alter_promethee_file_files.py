# Generated by Django 3.2.5 on 2021-09-17 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_ahp_file_promethee_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promethee_file',
            name='files',
            field=models.FileField(db_index=True, upload_to='uploads/'),
        ),
    ]