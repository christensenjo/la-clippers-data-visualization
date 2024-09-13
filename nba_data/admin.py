from django.contrib import admin
from .models import Team, Player, GameSchedule, Lineup, Roster, TeamAffiliate

admin.site.register(Team)
admin.site.register(Player)
admin.site.register(GameSchedule)
admin.site.register(Lineup)
admin.site.register(Roster)
admin.site.register(TeamAffiliate)