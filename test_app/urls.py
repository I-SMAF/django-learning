from django.urls import path

from .views import *

urlpatterns = [
    path('', TestView.as_view()),
    path('play/', TestPlayView.as_view()),
]
