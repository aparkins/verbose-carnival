from django.conf.urls import url
from dip_platform.api.game import game_api, adjudicate_api

urlpatterns = [
    url(r'^api/v1/game/(?P<game_id>\d+)/', game_api.GameView.as_view()),
    url(r'^api/v1/adjudicate/',            adjudicate_api.AdjudicateView.as_view()),
]
