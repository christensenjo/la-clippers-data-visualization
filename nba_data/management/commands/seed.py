import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
from nba_data.models import Team, Player, GameSchedule, Lineup, Roster, TeamAffiliate
from django.utils import timezone
import pytz
from datetime import datetime

class Command(BaseCommand):
    help = 'Seed database with data from JSON files'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting data import...')
        
        functions = [
            self.load_teams,
            self.load_players,
            self.load_game_schedules,
            self.load_rosters,
            self.load_lineups,
            self.load_team_affiliates
        ]
        
        for func in functions:
            func()
        
        self.stdout.write(self.style.SUCCESS('Data import completed successfully!'))

    def load_data(self, file_name, model_class, field_mappings):
        file_path = os.path.join(settings.BASE_DIR, 'dev_test_data', file_name)
        self.stdout.write(f'Loading data from {file_name}...')
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            with transaction.atomic():
                objects = []
                for item in data:
                    obj_data = {django_field: item[json_field] for django_field, json_field in field_mappings.items()}
                    objects.append(model_class(**obj_data))
                
                model_class.objects.bulk_create(objects, ignore_conflicts=True)
            
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(objects)} {model_class.__name__} objects'))
        
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f'File {file_name} not found'))
        except json.JSONDecodeError:
            self.stderr.write(self.style.ERROR(f'Invalid JSON in {file_name}'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error loading {file_name}: {str(e)}'))

    def load_teams(self):
        self.load_data('team.json', Team, {
            'team_id': 'teamId',
            'league_lk': 'leagueLk',
            'team_name': 'teamName',
            'team_name_short': 'teamNameShort',
            'team_nickname': 'teamNickname'
        })

    def load_players(self):
        self.load_data('player.json', Player, {
            'player_id': 'player_id',
            'first_name': 'first_name',
            'last_name': 'last_name'
        })

    # We handle the game schedule data differently so that we can convert datetime data to be timezone aware and prevent warnings
    def load_game_schedules(self):
        file_path = os.path.join(settings.BASE_DIR, 'dev_test_data', 'game_schedule.json')
        self.stdout.write(f'Loading data from game_schedule.json...')
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            with transaction.atomic():
                objects = []
                for item in data:
                    # Convert the naive datetime to an aware datetime
                    naive_datetime = datetime.strptime(item['game_date'], '%Y-%m-%d %H:%M:%S')
                    aware_datetime = timezone.make_aware(naive_datetime, timezone=pytz.UTC)
                    
                    obj_data = {
                        'game_id': item['game_id'],
                        'home_id': item['home_id'],
                        'home_score': item['home_score'],
                        'away_id': item['away_id'],
                        'away_score': item['away_score'],
                        'game_date': aware_datetime
                    }
                    objects.append(GameSchedule(**obj_data))
                
                GameSchedule.objects.bulk_create(objects, ignore_conflicts=True)
            
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(objects)} GameSchedule objects'))
        
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error loading game_schedule.json: {str(e)}'))

    def load_lineups(self):
        self.load_data('lineup.json', Lineup, {
            'team_id': 'team_id',
            'player_id': 'player_id',
            'lineup_num': 'lineup_num',
            'period': 'period',
            'game_id': 'game_id',
            'time_in': 'time_in',
            'time_out': 'time_out'
        })

    # We handle the roster data differently so that we can create players if they don't exist yet
    def load_rosters(self):
        file_path = os.path.join(settings.BASE_DIR, 'dev_test_data', 'roster.json')
        self.stdout.write(f'Loading data from roster.json...')
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            with transaction.atomic():
                roster_objects = []
                new_players = []
                for item in data:
                    team_id = item['team_id']
                    player_id = item['player_id']
                    
                    if not Player.objects.filter(player_id=player_id).exists():
                        # Create a new player if not exists
                        new_player = Player(
                            player_id=player_id,
                            first_name=item['first_name'],
                            last_name=item['last_name']
                        )
                        new_players.append(new_player)
                        self.stdout.write(self.style.WARNING(f'Creating new player: {new_player.first_name} {new_player.last_name} (ID: {new_player.player_id})'))
                    
                    if Team.objects.filter(team_id=team_id).exists():
                        roster_data = {
                            'team_id': team_id,
                            'player_id': player_id,
                            'position': item['position'],
                            'contract_type': item['contract_type']
                        }
                        roster_objects.append(Roster(**roster_data))
                    else:
                        self.stdout.write(self.style.WARNING(f'Skipping roster entry for team_id={team_id}, player_id={player_id} due to missing Team'))
                
                # Bulk create new players
                Player.objects.bulk_create(new_players, ignore_conflicts=True)
                
                # Bulk create roster entries
                Roster.objects.bulk_create(roster_objects, ignore_conflicts=True)
            
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(roster_objects)} Roster objects and created {len(new_players)} new Player objects'))
        
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error loading roster.json: {str(e)}'))

    # We handle the team affiliate data differently so that we can handle teams without a G League affiliate
    def load_team_affiliates(self):
        file_path = os.path.join(settings.BASE_DIR, 'dev_test_data', 'team_affiliate.json')
        self.stdout.write(f'Loading data from team_affiliate.json...')
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            with transaction.atomic():
                objects = []
                for item in data:
                    obj_data = {
                        'nba_team_id': item['nba_teamId'],
                        'nba_abrv': item['nba_abrv'],
                        'glg_team_id': item['glg_teamId'] if item['glg_teamId'] else None,
                        'glg_abrv': item['glg_abrv'] if item['glg_abrv'] else None
                    }
                    objects.append(TeamAffiliate(**obj_data))
                
                TeamAffiliate.objects.bulk_create(objects, ignore_conflicts=True)
            
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(objects)} TeamAffiliate objects'))
        
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error loading team_affiliate.json: {str(e)}'))