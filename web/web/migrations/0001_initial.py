# Generated by Django 2.1.7 on 2019-03-28 08:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id',
                 models.AutoField(
                     auto_created=True,
                     primary_key=True,
                     serialize=False,
                     verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('body', models.TextField()),
                ('date_published', models.DateTimeField(null=True)),
                ('date_scraped', models.DateTimeField()),
                ('url', models.URLField(max_length=600, unique=True)),
                ('classification_score', models.FloatField(null=True)),
                ('is_ground_truth', models.BooleanField(
                    default=False, null=True)),
            ],
            options={
                'db_table': 'article',
            },
        ),
        migrations.CreateModel(
            name='DateEntity',
            fields=[
                ('id',
                 models.AutoField(
                     auto_created=True,
                     primary_key=True,
                     serialize=False,
                     verbose_name='ID')),
                ('start_index', models.IntegerField()),
                ('end_index', models.IntegerField()),
                ('date_str', models.CharField(max_length=50)),
                ('date', models.DateTimeField(null=True)),
                ('seed',
                 models.ForeignKey(
                     on_delete=django.db.models.deletion.CASCADE,
                     related_name='date_entity',
                     to='web.Article')),
            ],
            options={
                'db_table': 'date_entity',
            },
        ),
        migrations.CreateModel(
            name='InjuredEntity',
            fields=[
                ('id',
                 models.AutoField(
                     auto_created=True,
                     primary_key=True,
                     serialize=False,
                     verbose_name='ID')),
                ('start_index', models.IntegerField()),
                ('end_index', models.IntegerField()),
                ('num_injured', models.IntegerField()),
                ('seed',
                 models.OneToOneField(
                     on_delete=django.db.models.deletion.CASCADE,
                     related_name='injured_entity',
                     to='web.Article')),
            ],
            options={
                'db_table': 'injured_entity',
            },
        ),
        migrations.CreateModel(
            name='KilledEntity',
            fields=[
                ('id',
                 models.AutoField(
                     auto_created=True,
                     primary_key=True,
                     serialize=False,
                     verbose_name='ID')),
                ('start_index', models.IntegerField()),
                ('end_index', models.IntegerField()),
                ('num_killed', models.IntegerField()),
                ('seed',
                 models.OneToOneField(
                     on_delete=django.db.models.deletion.CASCADE,
                     related_name='killed_entity',
                     to='web.Article')),
            ],
            options={
                'db_table': 'killed_entity',
            },
        ),
        migrations.CreateModel(
            name='LabelPost',
            fields=[
                ('id',
                 models.AutoField(
                     auto_created=True,
                     primary_key=True,
                     serialize=False,
                     verbose_name='ID')),
                ('urls', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'labelpost',
            },
        ),
        migrations.CreateModel(
            name='LocationEntity',
            fields=[
                ('id',
                 models.AutoField(
                     auto_created=True,
                     primary_key=True,
                     serialize=False,
                     verbose_name='ID')),
                ('start_index', models.IntegerField()),
                ('end_index', models.IntegerField()),
                ('location', models.CharField(max_length=200)),
                ('seed',
                 models.OneToOneField(
                     on_delete=django.db.models.deletion.CASCADE,
                     related_name='location_entity',
                     to='web.Article')),
            ],
            options={
                'db_table': 'location_entity',
            },
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id',
                 models.AutoField(
                     auto_created=True,
                     primary_key=True,
                     serialize=False,
                     verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('homepage', models.URLField(unique=True)),
                ('favicon', models.URLField(unique=True)),
            ],
            options={
                'db_table': 'source',
            },
        ),
        migrations.AddField(
            model_name='article',
            name='source',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to='web.Source'),
        ),
    ]
