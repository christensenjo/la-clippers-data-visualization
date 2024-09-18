import logging
from django.shortcuts import render
from django.http import JsonResponse
from .queries import get_team_records, get_team_records_for_month, get_raw_sql, get_available_months
import calendar

logger = logging.getLogger(__name__)

def index_view(request):
    return render(request, 'base.html')

def team_records_api(request):
    year = request.GET.get('year')
    month = request.GET.get('month')
    
    if year and month:
        records = get_team_records_for_month(int(year), int(month))
    else:
        records = get_team_records()
    
    data = list(records.values(
        'team_name', 'win_percentage', 'total_wins', 'total_losses',
        'total_games_played', 'total_home_games', 'total_away_games'
    ))
    return JsonResponse(data, safe=False)

def team_records_sql_api(request):
    year = request.GET.get('year')
    month = request.GET.get('month')
    
    if year and month:
        query = get_team_records_for_month(int(year), int(month))
    else:
        query = get_team_records()
    
    sql = get_raw_sql(query)
    return JsonResponse({'sql_query': sql})

def available_months_api(request):
    months = get_available_months()
    data = [{'value': f"{month['year']}-{int(month['month']):02d}", 
            'label': f"{month['year']} {calendar.month_name[int(month['month'])]}"}
            for month in months]
    return JsonResponse(data, safe=False)
