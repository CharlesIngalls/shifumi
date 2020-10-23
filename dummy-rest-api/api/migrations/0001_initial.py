# Generated by Django 3.0 on 2020-10-09 14:07

import api.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_started', models.BooleanField(default=False)),
                ('acces_a', models.IntegerField(default=api.models.randomint)),
                ('acces_b', models.IntegerField(default=api.models.randomint)),
            ],
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Game')),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_played', models.CharField(choices=[('ROCK', 'Rock'), ('PAPER', 'Paper'), ('SCISSOR', 'Scissor')], max_length=7)),
                ('round', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Round')),
            ],
        ),
    ]