from django.db import models

class Team(models.Model):
    team_id = models.BigIntegerField(primary_key=True)
    league_lk = models.CharField(max_length=3)
    team_name = models.CharField(max_length=100)
    team_name_short = models.CharField(max_length=4)
    team_nickname = models.CharField(max_length=50)

    class Meta:
        db_table = 'team'

    def __str__(self):
        return self.team_name

class Player(models.Model):
    player_id = models.BigIntegerField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'player'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class GameSchedule(models.Model):
    game_id = models.BigIntegerField(primary_key=True)
    home = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_games')
    away = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_games')
    home_score = models.IntegerField()
    away_score = models.IntegerField()
    game_date = models.DateTimeField()

    class Meta:
        db_table = 'game_schedule'

    def __str__(self):
        return f"Game {self.game_id}: {self.home} vs {self.away} on {self.game_date}"

class Lineup(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    lineup_num = models.IntegerField()
    period = models.IntegerField()
    time_in = models.FloatField()
    time_out = models.FloatField()
    game = models.ForeignKey(GameSchedule, on_delete=models.CASCADE)

    class Meta:
        db_table = 'lineup'
        unique_together = ('team', 'player', 'lineup_num', 'period', 'game')

    def __str__(self):
        return f"Lineup {self.lineup_num} for {self.team} in game {self.game_id}"

class Roster(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    position = models.CharField(max_length=2)
    contract_type = models.CharField(max_length=20)

    class Meta:
        db_table = 'roster'
        unique_together = ('team', 'player')

    def __str__(self):
        return f"{self.player} on {self.team}"

class TeamAffiliate(models.Model):
    nba_team = models.OneToOneField(Team, on_delete=models.CASCADE, primary_key=True)
    nba_abrv = models.CharField(max_length=3)
    glg_team_id = models.BigIntegerField(null=True, blank=True)  # Not all NBA teams have a G League affiliate
    glg_abrv = models.CharField(max_length=3, null=True, blank=True)

    class Meta:
        db_table = 'team_affiliate'

    def __str__(self):
        return f"{self.nba_abrv} - {self.glg_abrv or 'No G League Affiliate'}"