from django.contrib import admin

from .models import Team, Match, Game
# Register your models here.

admin.site.register(Team)
admin.site.register(Match)
admin.site.register(Game)
