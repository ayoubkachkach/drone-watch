# Generated by Django 2.1.7 on 2019-04-02 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0011_locationentity_region'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='locationentity',
            name='end_index',
        ),
        migrations.RemoveField(
            model_name='locationentity',
            name='start_index',
        ),
        migrations.AddField(
            model_name='locationentity',
            name='country_end_index',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='locationentity',
            name='country_start_index',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='locationentity',
            name='region_end_index',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='locationentity',
            name='region_start_index',
            field=models.IntegerField(null=True),
        ),
    ]
