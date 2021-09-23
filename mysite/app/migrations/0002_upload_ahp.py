# Generated by Django 3.2.5 on 2021-09-21 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Upload_ahp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
                ('path', models.FileField(default='default_ahp.csv', null=True, upload_to='ahp/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='upload_ahps', to='app.profile')),
            ],
        ),
    ]