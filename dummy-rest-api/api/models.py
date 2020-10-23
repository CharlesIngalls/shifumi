from django.db import models
import random

from django.utils.translation import gettext_lazy as _


def randomint():
    return random.randint(1000000, 9999999)


class Game(models.Model):
    is_started = models.BooleanField(default=False)
    access_a = models.IntegerField(default=randomint)
    access_b = models.IntegerField(default=randomint)

    def get_active_round_id(self):
        round = Round.objects.filter(game__id=self.id).filter(over=False).first()
        return round.id


class Round(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    over = models.BooleanField(default=False)
    is_draw = models.BooleanField(default=False)
    is_A_winner = models.BooleanField(default=False)
    a_has_played = models.BooleanField(default=False)
    b_has_played = models.BooleanField(default=False)



class Choice(models.Model):
    class Type(models.TextChoices):
        ROCK = 'ROCK', _('Rock')
        PAPER = 'PAPER', _('Paper')
        SCISSOR = 'SCISSOR', _('Scissor')

    choice_played = models.CharField(max_length=7, choices=Type.choices)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    is_player_A = models.BooleanField()