# Generated by Django 3.0 on 2020-10-09 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_choice_is_player_a'),
    ]

    operations = [
        migrations.AddField(
            model_name='round',
            name='over',
            field=models.BooleanField(default=False),
        ),
    ]
