# Generated by Django 3.2.4 on 2021-06-23 19:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.RemoveField(
            model_name='vaccins',
            name='Characteristiques',
        ),
        migrations.RemoveField(
            model_name='vaccins',
            name='cout',
        ),
        migrations.RemoveField(
            model_name='vaccins',
            name='effets_secondaires',
        ),
        migrations.RemoveField(
            model_name='vaccins',
            name='posologie',
        ),
        migrations.DeleteModel(
            name='Characteristiques',
        ),
        migrations.DeleteModel(
            name='Cout',
        ),
        migrations.DeleteModel(
            name='Effets_secondaires',
        ),
        migrations.DeleteModel(
            name='Posologie',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
        migrations.DeleteModel(
            name='vaccins',
        ),
    ]