from django.core.management.base import BaseCommand
from django.db import transaction
from nba_data.models import Team, Player, GameSchedule, Lineup, Roster, TeamAffiliate
import json
import os
from django.conf import settings
from django.utils import timezone
import pytz
from datetime import datetime

class Command(BaseCommand):
    help = 'Update database with new data from JSON files'

    def handle(self, *args, **options):
        self.stdout.write('Starting data update...')
        
        update_functions = [
            self.update_teams,
            self.update_players,
            self.update_game_schedules,
            self.update_rosters,
            self.update_lineups,
            self.update_team_affiliates
        ]
        
        for func in update_functions:
            func()
        
        self.stdout.write(self.style.SUCCESS('Data update completed successfully!'))

    def load_json(self, file_name):
        file_path = os.path.join(settings.BASE_DIR, 'dev_test_data', file_name)
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f'File {file_name} not found'))
            return []
        except json.JSONDecodeError:
            self.stderr.write(self.style.ERROR(f'Invalid JSON in {file_name}'))
            return []

    # We'll add individual update methods for each model here

    def update_teams(self):
        data = self.load_json('team.json')
        self.stdout.write('Updating teams...')
        
        with transaction.atomic():
            for item in data:
                Team.objects.update_or_create(
                    team_id=item['teamId'],
                    defaults={
                        'league_lk': item['leagueLk'],
                        'team_name': item['teamName'],
                        'team_name_short': item['teamNameShort'],
                        'team_nickname': item['teamNickname']
                    }
                )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {len(data)} Team objects'))

    def update_players(self):
        data = self.load_json('player.json')
        self.stdout.write('Updating players...')
        
        with transaction.atomic():
            for item in data:
                Player.objects.update_or_create(
                    player_id=item['player_id'],
                    defaults={
                        'first_name': item['first_name'],
                        'last_name': item['last_name']
                    }
                )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {len(data)} Player objects'))

    def update_game_schedules(self):
        data = self.load_json('game_schedule.json')
        self.stdout.write('Updating game schedules...')
        
        with transaction.atomic():
            for item in data:
                naive_datetime = datetime.strptime(item['game_date'], '%Y-%m-%d %H:%M:%S')
                aware_datetime = timezone.make_aware(naive_datetime, timezone=pytz.UTC)
                
                GameSchedule.objects.update_or_create(
                    game_id=item['game_id'],
                    defaults={
                        'home_id': item['home_id'],
                        'home_score': item['home_score'],
                        'away_id': item['away_id'],
                        'away_score': item['away_score'],
                        'game_date': aware_datetime
                    }
                )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {len(data)} GameSchedule objects'))

    def update_lineups(self):
        data = self.load_json('lineup.json')
        self.stdout.write('Updating lineups...')
        
        with transaction.atomic():
            for item in data:
                Lineup.objects.update_or_create(
                    team_id=item['team_id'],
                    player_id=item['player_id'],
                    lineup_num=item['lineup_num'],
                    period=item['period'],
                    game_id=item['game_id'],
                    defaults={
                        'time_in': item['time_in'],
                        'time_out': item['time_out']
                    }
                )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {len(data)} Lineup objects'))

    def update_rosters(self):
        data = self.load_json('roster.json')
        self.stdout.write('Updating rosters...')
        
        with transaction.atomic():
            for item in data:
                player, _ = Player.objects.update_or_create(
                    player_id=item['player_id'],
                    defaults={
                        'first_name': item['first_name'],
                        'last_name': item['last_name']
                    }
                )
                
                Roster.objects.update_or_create(
                    team_id=item['team_id'],
                    player_id=item['player_id'],
                    defaults={
                        'position': item['position'],
                        'contract_type': item['contract_type']
                    }
                )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {len(data)} Roster objects'))

    def update_team_affiliates(self):
        data = self.load_json('team_affiliate.json')
        self.stdout.write('Updating team affiliates...')
        
        with transaction.atomic():
            for item in data:
                TeamAffiliate.objects.update_or_create(
                    nba_team_id=item['nba_teamId'],
                    defaults={
                        'nba_abrv': item['nba_abrv'],
                        'glg_team_id': item['glg_teamId'] if item['glg_teamId'] else None,
                        'glg_abrv': item['glg_abrv'] if item['glg_abrv'] else None
                    }
                )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {len(data)} TeamAffiliate objects'))
