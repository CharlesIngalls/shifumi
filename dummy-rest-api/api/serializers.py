from rest_framework import serializers
from django.contrib.auth import get_user_model

from api.models import Game, Choice, Round
from django.db.models import Q

User = get_user_model()


class UserBaseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'first_name', 'last_name', 'username', 'email']


class GameSerializer(serializers.ModelSerializer):

    old_rounds = serializers.SerializerMethodField()
    can_A_play = serializers.SerializerMethodField()
    can_B_play = serializers.SerializerMethodField()

    def get_old_rounds(self, obj):
        qs = Round.objects.filter(game__id=obj.id).filter(over=True)
        return RoundSerializer(qs, many=True).data

    def get_can_A_play(self, obj):
        round = Round.objects.filter(game_id=obj.id).filter(over=False).first()
        if round is None: # game over
            return False
        return not round.a_has_played

    def get_can_B_play(self, obj):
        round = Round.objects.filter(game_id=obj.id).filter(over=False).first()
        if round is None: # game over
            return False
        return not round.b_has_played

    def create(self, validated_data):
        game = Game.objects.create()
        Round.objects.create(game=game)
        return game

    class Meta:
        model = Game
        fields = ['id', 'is_started', 'access_a', 'access_b', 'points_to_win', 'is_started', 'old_rounds',
                  'can_A_play', 'can_B_play', 'is_over']


class RoundSerializer(serializers.ModelSerializer):

    choices = serializers.SerializerMethodField()

    def get_choices(self, obj):
        qs = Choice.objects.filter(round_id=obj.id)
        return ChoiceSerializer(qs, many=True).data

    class Meta:
        model = Round
        fields = ['id', 'game', 'choices', 'over', 'is_A_winner', 'is_draw', 'a_has_played', 'b_has_played']


class ChoiceSerializer(serializers.ModelSerializer):

    access_id = serializers.IntegerField(write_only=True)
    is_player_A = serializers.BooleanField(read_only=True)

    def create(self, validated_data):

        access_id = validated_data.pop('access_id')
        game = Game.objects.get(Q(access_a=access_id) | Q(access_b=access_id))
        round = Round.objects.get(id=game.get_active_round_id())
        validated_data['round'] = round

        is_player_A = False
        if game.access_a == access_id:
            is_player_A = True

        if is_player_A:
            validated_data['is_player_A'] = True
            round.a_has_played = True
        else:
            validated_data['is_player_A'] = False
            round.b_has_played = True


        choice = Choice.objects.create(**validated_data)

        if Choice.objects.filter(round_id=round.id).count() == 2: # if both players played

            other_choice = Choice.objects.filter(round_id=round.id).exclude(id=choice.id).first()

            if other_choice.choice_played == choice.choice_played:
                round.is_draw = True

            if choice.choice_played == Choice.Type.PAPER and other_choice.choice_played == Choice.Type.ROCK:
                if is_player_A:
                    round.is_A_winner = True
            if choice.choice_played == Choice.Type.ROCK and other_choice.choice_played == Choice.Type.SCISSOR:
                if is_player_A:
                    round.is_A_winner = True
            if choice.choice_played == Choice.Type.SCISSOR and other_choice.choice_played == Choice.Type.PAPER:
                if is_player_A:
                    round.is_A_winner = True
            if choice.choice_played == Choice.Type.PAPER and other_choice.choice_played == Choice.Type.SCISSOR:
                if not is_player_A:
                    round.is_A_winner = True
            if choice.choice_played == Choice.Type.ROCK and other_choice.choice_played == Choice.Type.PAPER:
                if not is_player_A:
                    round.is_A_winner = True
            if choice.choice_played == Choice.Type.SCISSOR and other_choice.choice_played == Choice.Type.ROCK:
                if not is_player_A:
                    round.is_A_winner = True
            round.over = True
        round.save()

        rounds = Round.objects.filter(game_id=game.id).filter(over=True)

        nb_rounds_won_by_A = len([round for round in rounds if round.is_A_winner])
        nb_rounds_won_by_B = len([round for round in rounds if not round.is_A_winner and not round.is_draw])

        print(nb_rounds_won_by_A)
        print(nb_rounds_won_by_B)

        if nb_rounds_won_by_A >= game.points_to_win or nb_rounds_won_by_B >= game.points_to_win:
            game.is_over = True
            game.save()

        if not game.is_over and Choice.objects.filter(round_id=round.id).count() == 2:
            Round.objects.create(game=round.game)

        return choice

    class Meta:
        model = Choice
        fields = ['id', 'choice_played', 'is_player_A', 'access_id']
