from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, mixins, GenericViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, permissions

from api.models import Game, Choice, Round
from api.serializers import UserBaseSerializer, GameSerializer, ChoiceSerializer, RoundSerializer

from django.db.models import Q

User = get_user_model()


class UserViewSet(NestedViewSetMixin, ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserBaseSerializer


class UserSelfView(APIView):

    def get(self, request, format=None):
        serializer = UserBaseSerializer(request.user, context={'request': request})
        return Response(serializer.data)


class Play(APIView):

    def get(self, request, access_id):
        game = Game.objects.filter(Q(access_a=access_id) | Q(access_b=access_id)).first()
        if game is None:
            return Response({})
        return Response(GameSerializer(game).data)


class GameViewSet(viewsets.ModelViewSet):
    serializer_class = GameSerializer
    queryset = Game.objects.all()


class RoundViewSet(viewsets.ModelViewSet):
    serializer_class = RoundSerializer
    queryset = Round.objects.all()


class CanPlay(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            game = Game.objects.get(Q(access_a=request.data['access_id']) | Q(access_b=request.data['access_id']))
            round = Round.objects.get(id=game.get_active_round_id())

            is_player_A = False

            if game.access_a == int(request.data['access_id']):
                is_player_A = True

            if is_player_A:
                return not round.a_has_played

            return not round.b_has_played

        return True


class ChoiceViewSet(viewsets.ModelViewSet):
    permission_classes = [CanPlay, ]
    serializer_class = ChoiceSerializer
    queryset = Choice.objects.all()
