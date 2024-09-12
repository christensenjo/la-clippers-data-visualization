# Tables

## game_schedule
231 records

Column names:
['game_id', 'home_id', 'home_score', 'away_id', 'away_score', 'game_date']

Primary key: game_id

```
   game_id     home_id  home_score     away_id  away_score             game_date
0        1  1610612752         112  1610612750         106   2024-01-01 15:00:00  
1        2  1610612761         124  1610612739         121   2024-01-01 19:30:00 
2        3  1610612745         136  1610612765         113   2024-01-01 20:00:00 
3        4  1610612749         113  1610612754         122   2024-01-01 20:00:00  
4        5  1610612743         111  1610612766          93   2024-01-01 21:00:00 
```

## lineup
117,040 records

Column names:
['team_id', 'player_id', 'lineup_num', 'period', 'time_in', 'time_out', 'game_id']

Primary key: team_id, player_id, lineup_num, period

```
      team_id  player_id  lineup_num  period  time_in  time_out  game_id
0  1610612737    1629027           1       1    720.0     456.0       17
1  1610612737    1629027           2       1    456.0     456.0       17
2  1610612737    1629027           3       1    456.0     383.0       17
3  1610612737    1629027           9       1    189.0     165.0       17
4  1610612737    1629027          10       1    165.0     165.0       17
```

## player
480 records

Column names:
['player_id', 'first_name', 'last_name']

Primary key: player_id

```
   player_id first_name   last_name
0    1626246      Boban  Marjanovic
1    1627742    Brandon      Ingram
2    1627749   Dejounte      Murray
3    1627752    Taurean      Prince
4    1630164      James     Wiseman
```

## roster
63 records

Column names:
['team_id', 'player_id', 'first_name', 'last_name', 'position', 'contract_type']

Primary key: team_id, player_id

```
      team_id  player_id first_name   last_name position contract_type
0  1610612737     202083     Wesley    Matthews       SG           NBA
1  1610612737     203991      Clint      Capela        C           NBA
2  1610612737     203992     Bogdan  Bogdanovic       SG           NBA
3  1610612737    1627749   Dejounte      Murray       PG           NBA
4  1610612737    1628981      Bruno    Fernando        C           NBA
```

## team
62 records

Column names:
['teamId', 'leagueLk', 'teamName', 'teamNameShort', 'teamNickname']

Primary key: teamId

```
       teamId leagueLk              teamName teamNameShort teamNickname
0  1610612737      NBA         Atlanta Hawks           ATL        Hawks
1  1610612738      NBA        Boston Celtics           BOS      Celtics
2  1610612739      NBA   Cleveland Cavaliers           CLE    Cavaliers
3  1610612740      NBA  New Orleans Pelicans           NOP     Pelicans
4  1610612741      NBA         Chicago Bulls           CHI        Bulls
```

## team_affiliate
30 records

Column names:
['nba_teamId', 'nba_abrv', 'glg_teamId', 'glg_abrv']

Primary key: nba_teamId

```
   nba_teamId nba_abrv    glg_teamId glg_abrv
0  1610612737      ATL  1.612710e+09      CPS
1  1610612751      BKN  1.612710e+09      LIN
2  1610612738      BOS  1.612710e+09      MNE
3  1610612766      CHA  1.612710e+09      GBO
4  1610612741      CHI  1.612710e+09      WCB
```