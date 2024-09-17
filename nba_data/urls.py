from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('api/team-records/', views.team_records_api, name='team_records_api'),
]
