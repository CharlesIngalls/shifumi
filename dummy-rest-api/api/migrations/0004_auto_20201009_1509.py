# Generated by Django 3.0 on 2020-10-09 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_round_over'),
    ]

    operations = [
        migrations.AddField(
            model_name='round',
            name='is_A_winner',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='round',
            name='is_draw',
            field=models.BooleanField(default=False),
        ),
    ]
