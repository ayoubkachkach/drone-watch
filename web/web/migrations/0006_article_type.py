# Generated by Django 2.1.7 on 2019-03-31 08:10

from django.db import migrations, models
import web.models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_auto_20190330_0732'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='type',
            field=models.CharField(choices=[(web.models.Types('NOT_DRONE'), 'NOT_DRONE'), (web.models.Types('STRIKE'), 'STRIKE'), (web.models.Types('MANY_STRIKES'), 'MANY_STRIKES'), (web.models.Types('EDITORIAL'), 'EDITORIAL')], max_length=20, null=True),
        ),
    ]