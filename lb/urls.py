from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.hello),
    # TODO: Config URL Patterns
    path('leaderboard', views.leaderboard),
    path('history/<slug:username>', views.history),
    path('submit', views.submit),
    path('vote', views.vote)
]
