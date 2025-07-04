# Generated by Django 5.2.3 on 2025-06-14 16:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('release_year', models.IntegerField()),
                ('status', models.CharField(choices=[('plan', 'planned to watch'), ('watched', 'watched'), ('watching', 'watching')], max_length=100)),
                ('rating', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Movies',
            fields=[
                ('film_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='watchlist.film')),
                ('movie_length', models.IntegerField(default=0)),
            ],
            bases=('watchlist.film',),
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('film_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='watchlist.film')),
                ('current_episode', models.IntegerField()),
                ('number_of_seasons', models.IntegerField()),
                ('number_of_episodes', models.IntegerField()),
                ('next_release_date', models.CharField(choices=[('unknown', 'to be determined'), ('completed', 'finished airing')], max_length=100)),
            ],
            bases=('watchlist.film',),
        ),
    ]
