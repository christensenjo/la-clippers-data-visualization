from django.urls import path
from . import views

urlpatterns = [
    path('team-records/', views.team_records_view, name='team_records'),
]
