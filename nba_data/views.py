import logging
from django.shortcuts import render
from django.http import JsonResponse
from .queries import get_team_records

logger = logging.getLogger(__name__)

def index_view(request):
    return render(request, 'base.html')

def team_records_api(request):
    records = get_team_records()
    data = list(records.values(
        'team_name', 'win_percentage', 'total_wins', 'total_losses',
        'total_games_played', 'total_home_games', 'total_away_games'
    ))
    return JsonResponse(data, safe=False)
