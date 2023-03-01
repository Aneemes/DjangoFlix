# Generated by Django 3.2.17 on 2023-03-01 15:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('playlists', '0006_auto_20230228_2349'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='order',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='playlist',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='playlists.playlist'),
        ),
    ]
