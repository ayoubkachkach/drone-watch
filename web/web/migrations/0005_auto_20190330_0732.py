# Generated by Django 2.1.7 on 2019-03-30 07:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web',
         '0004_dateentity_injuredentity_killedentity_labelpost_locationentity_perpetratorentity'
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name='dateentity',
            name='seed',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='date_entity',
                to='web.Article'),
        ),
    ]
