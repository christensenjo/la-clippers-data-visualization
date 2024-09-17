import logging
from django.shortcuts import render
from .queries import get_team_records, get_team_records_for_month, get_team_records_sql, get_team_records_for_month_sql
from datetime import datetime

logger = logging.getLogger(__name__)

def team_records_view(request):
    overall_records = get_team_records()
    current_month = datetime.now().month
    current_year = datetime.now().year
    monthly_records = get_team_records_for_month(current_year, current_month)
    
    # Log team records for debugging
    for record in overall_records:
        logger.debug(f"Team: {record.team_name}, Games: {record.total_games_played}, Wins: {record.total_wins}, Losses: {record.total_losses}, Win%: {record.win_percentage}")
    
    overall_sql = get_team_records_sql()
    monthly_sql = get_team_records_for_month_sql(current_year, current_month)
    context = {
        'overall_records': overall_records,
        'monthly_records': monthly_records,
        'current_month': current_month,
        'current_year': current_year,
        'overall_sql': overall_sql,
        'monthly_sql': monthly_sql,
    }
    return render(request, 'nba_data/team_records.html', context)
