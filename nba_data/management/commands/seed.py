import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from nba_data.models import Team, Player, GameSchedule, Lineup, Roster, TeamAffiliate

class Command(BaseCommand):
    help = 'Seed database with data from JSON files'
    
    def handle(self, *args, **kwargs):
        self.load_teams()
        self.load_players()
        self.load_game_schedules()
        self.load_lineups()
        self.load_rosters()
        self.load_team_affiliates()
    
    def load_teams(self):
        file_path = os.path.join(settings.BASE_DIR, 'dev_test_data', 'team.json')
        with open(file_path, 'r') as f:
            teams_data = json.load(f)
        
        for team in teams_data:
            Team.objects.create(
                team_id=team['teamId'],
                league_lk=team['leagueLk'],
                team_name=team['teamName'],
                team_name_short=team['teamNameShort'],
                team_nickname=team['teamNickname']
            )
            
    def load_players(self):
        file_path = os.path.join(settings.BASE_DIR, 'dev_test_data', 'player.json')
        with open(file_path, 'r') as f:
            players_data = json.load(f)
        
        for player in players_data:
            Player.objects.create(
                player_id=player['player_id'],
                first_name=player['first_name'],
                last_name=player['last_name']
            )
            
    def load_game_schedules(self):
        file_path = os.path.join(settings.BASE_DIR, 'dev_test_data', 'game_schedule.json')
        with open(file_path, 'r') as f:
            game_schedules_data = json.load(f)
            
        for game_schedule in game_schedules_data:
            GameSchedule.objects.create(
                game_id=game_schedule['game_id'],
                home_id=game_schedule['home_id'],
                home_score=game_schedule['home_score'],
                away_id=game_schedule['away_id'],
                away_score=game_schedule['away_score'],
                game_date=game_schedule['game_date']
            )
        
        
    def load_lineups(self):
        file_path = os.path.join(settings.BASE_DIR, 'dev_test_data', 'lineup.json')
        with open(file_path, 'r') as f:
            lineups_data = json.load(f)
            
        for lineup in lineups_data:
            Lineup.objects.create(
                team_id=lineup['team_id'],
                player_id=lineup['player_id'],
                lineup_num=lineup['lineup_num'],
                period=lineup['period'],
                game_id=lineup['game_id'],
                time_in=lineup['time_in'],
                time_out=lineup['time_out']
            )
        
    def load_rosters(self):
        file_path = os.path.join(settings.BASE_DIR, 'dev_test_data', 'roster.json')
        with open(file_path, 'r') as f:
            rosters_data = json.load(f)
        
        for roster in rosters_data:
            Roster.objects.create(
                team_id=roster['team_id'],
                player_id=roster['player_id'],
                position=roster['position'],
                contract_type=roster['contract_type']
            )
        
    def load_team_affiliates(self):
        file_path = os.path.join(settings.BASE_DIR, 'dev_test_data', 'team_affiliate.json')
        with open(file_path, 'r') as f:
            team_affiliates_data = json.load(f)
        
        for team_affiliate in team_affiliates_data:
            TeamAffiliate.objects.create(
                nba_team_id=team_affiliate['nba_team_id'],
                nba_abrv=team_affiliate['nba_abrv'],
                glg_team_id=team_affiliate['glg_team_id'],
                glg_abrv=team_affiliate['glg_abrv']
            )
            
