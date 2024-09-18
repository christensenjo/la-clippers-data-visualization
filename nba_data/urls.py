from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('api/team-records/', views.team_records_api, name='team_records_api'),
    path('api/team-records-sql/', views.team_records_sql_api, name='team_records_sql_api'),
    path('api/available-months/', views.available_months_api, name='available_months_api'),
]
