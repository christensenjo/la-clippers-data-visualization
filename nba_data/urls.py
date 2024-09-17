from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('team-records/', views.team_records_view, name='team_records'),
]
