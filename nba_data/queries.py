from django.db.models import Count, F, Window, Case, When, Value, IntegerField, FloatField
from django.db.models.functions import DenseRank
from .models import Team, GameSchedule
from django.db import connection
from django.http import JsonResponse

def get_team_records():
    return Team.objects.annotate(
        total_games_played=Count('home_games') + Count('away_games'),
        total_wins=Count(Case(
            When(home_games__home_score__gt=F('home_games__away_score'), then=1),
            When(away_games__away_score__gt=F('away_games__home_score'), then=1),
        )),
        total_losses=F('total_games_played') - F('total_wins'),
        win_percentage=Case(
            When(total_games_played=0, then=Value(0.0)),
            default=F('total_wins') * 1.0 / F('total_games_played'),
            output_field=FloatField()
        ),
        total_home_games=Count('home_games'),
        total_away_games=Count('away_games'),
        games_played_rank=Window(
            expression=DenseRank(),
            order_by=F('total_games_played').desc()
        ),
        home_games_rank=Window(
            expression=DenseRank(),
            order_by=F('total_home_games').desc()
        ),
        away_games_rank=Window(
            expression=DenseRank(),
            order_by=F('total_away_games').desc()
        )
    ).order_by('-win_percentage')

def get_team_records_for_month(year, month):
    return Team.objects.annotate(
        total_games_played=Count(Case(
            When(home_games__game_date__year=year, home_games__game_date__month=month, then=1),
            When(away_games__game_date__year=year, away_games__game_date__month=month, then=1),
        )),
        total_wins=Count(Case(
            When(home_games__game_date__year=year, home_games__game_date__month=month, 
                home_games__home_score__gt=F('home_games__away_score'), then=1),
            When(away_games__game_date__year=year, away_games__game_date__month=month, 
                away_games__away_score__gt=F('away_games__home_score'), then=1),
        )),
        total_losses=F('total_games_played') - F('total_wins'),
        win_percentage=Case(
            When(total_games_played=0, then=Value(0.0)),
            default=F('total_wins') * 1.0 / F('total_games_played'),
            output_field=FloatField()
        ),
        total_home_games=Count(Case(
            When(home_games__game_date__year=year, home_games__game_date__month=month, then=1),
        )),
        total_away_games=Count(Case(
            When(away_games__game_date__year=year, away_games__game_date__month=month, then=1),
        )),
        games_played_rank=Window(
            expression=DenseRank(),
            order_by=F('total_games_played').desc()
        ),
        home_games_rank=Window(
            expression=DenseRank(),
            order_by=F('total_home_games').desc()
        ),
        away_games_rank=Window(
            expression=DenseRank(),
            order_by=F('total_away_games').desc()
        )
    ).order_by('-win_percentage')

def get_raw_sql(queryset):
    """Get the raw SQL for a queryset."""
    return str(queryset.query)

def get_team_records_sql():
    """Raw SQL query for team records and rankings."""
    sql = """
    WITH team_stats AS (
        SELECT 
            t.team_id,
            t.team_name,
            COUNT(DISTINCT CASE WHEN g.home_id = t.team_id THEN g.game_id
                                WHEN g.away_id = t.team_id THEN g.game_id END) as games_played,
            COUNT(DISTINCT CASE WHEN (g.home_id = t.team_id AND g.home_score > g.away_score) OR
                                    (g.away_id = t.team_id AND g.away_score > g.home_score) 
                            THEN g.game_id END) as wins,
            COUNT(DISTINCT CASE WHEN g.home_id = t.team_id THEN g.game_id END) as home_games,
            COUNT(DISTINCT CASE WHEN g.away_id = t.team_id THEN g.game_id END) as away_games
        FROM 
            nba_data_team t
        LEFT JOIN 
            nba_data_gameschedule g ON t.team_id = g.home_id OR t.team_id = g.away_id
        GROUP BY 
            t.team_id, t.team_name
    )
    SELECT 
        team_name,
        games_played,
        wins,
        (games_played - wins) as losses,
        CASE WHEN games_played = 0 THEN 0
            ELSE CAST(wins AS FLOAT) / games_played 
        END as win_percentage,
        home_games,
        away_games,
        DENSE_RANK() OVER (ORDER BY games_played DESC) as games_played_rank,
        DENSE_RANK() OVER (ORDER BY home_games DESC) as home_games_rank,
        DENSE_RANK() OVER (ORDER BY away_games DESC) as away_games_rank
    FROM 
        team_stats
    ORDER BY 
        win_percentage DESC;
    """
    return sql

def get_team_records_for_month_sql(year, month):
    """Raw SQL query for team records and rankings for a specific month."""
    sql = f"""
    WITH team_stats AS (
        SELECT 
            t.team_id,
            t.team_name,
            COUNT(DISTINCT CASE WHEN (g.home_id = t.team_id OR g.away_id = t.team_id) 
                                    AND EXTRACT(YEAR FROM g.game_date) = {year}
                                    AND EXTRACT(MONTH FROM g.game_date) = {month}
                            THEN g.game_id END) as games_played,
            COUNT(DISTINCT CASE WHEN ((g.home_id = t.team_id AND g.home_score > g.away_score) OR
                                    (g.away_id = t.team_id AND g.away_score > g.home_score))
                                    AND EXTRACT(YEAR FROM g.game_date) = {year}
                                    AND EXTRACT(MONTH FROM g.game_date) = {month}
                            THEN g.game_id END) as wins,
            COUNT(DISTINCT CASE WHEN g.home_id = t.team_id 
                                    AND EXTRACT(YEAR FROM g.game_date) = {year}
                                    AND EXTRACT(MONTH FROM g.game_date) = {month}
                            THEN g.game_id END) as home_games,
            COUNT(DISTINCT CASE WHEN g.away_id = t.team_id 
                                    AND EXTRACT(YEAR FROM g.game_date) = {year}
                                    AND EXTRACT(MONTH FROM g.game_date) = {month}
                            THEN g.game_id END) as away_games
        FROM 
            nba_data_team t
        LEFT JOIN 
            nba_data_gameschedule g ON t.team_id = g.home_id OR t.team_id = g.away_id
        GROUP BY 
            t.team_id, t.team_name
    )
    SELECT 
        team_name,
        games_played,
        wins,
        (games_played - wins) as losses,
        CASE WHEN games_played = 0 THEN 0
            ELSE CAST(wins AS FLOAT) / games_played 
        END as win_percentage,
        home_games,
        away_games,
        DENSE_RANK() OVER (ORDER BY games_played DESC) as games_played_rank,
        DENSE_RANK() OVER (ORDER BY home_games DESC) as home_games_rank,
        DENSE_RANK() OVER (ORDER BY away_games DESC) as away_games_rank
    FROM 
        team_stats
    ORDER BY 
        win_percentage DESC;
    """
    return sql

def execute_raw_sql(sql):
    """Execute a raw SQL query and return the results."""
    with connection.cursor() as cursor:
        cursor.execute(sql)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

def team_records_api(request):
    records = get_team_records()
    data = list(records.values(
        'team_name', 'total_games_played', 'total_wins', 'total_losses', 'win_percentage',
        'total_home_games', 'total_away_games', 'games_played_rank', 'home_games_rank', 'away_games_rank'
    ))
    return JsonResponse(data, safe=False)
