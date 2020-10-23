from django.urls import path
from rest_framework_extensions.routers import ExtendedSimpleRouter as SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from api.views import UserViewSet, UserSelfView, GameViewSet, ChoiceViewSet, RoundViewSet, Play

router = SimpleRouter()

user_list = router.register('users', UserViewSet, basename="user")
user_list = router.register('games', GameViewSet, basename="game")
user_list = router.register('rounds', RoundViewSet, basename="round")
user_list = router.register('choices', ChoiceViewSet, basename="choice")


urlpatterns = router.urls
urlpatterns.append(path('login/', TokenObtainPairView.as_view()))
urlpatterns.append(path('user/', UserSelfView.as_view()))
urlpatterns.append(path('play/<int:access_id>/', Play.as_view()))
