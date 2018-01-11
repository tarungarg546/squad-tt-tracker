from django.contrib import admin

from .models import Team, Match, Game


class GameInline(admin.TabularInline):
    model = Game
    extra = 1


class MatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'team_1', 'team_2', 'winner', 'started_at', 'ended_at')

    fieldsets = [
        (None,                  {'fields': ['category', 'team_1', 'team_2', 'winner']}),
        ('Date Information',    {'fields': ['started_at', 'ended_at']})
    ]
    inlines = [GameInline]


admin.site.register(Match, MatchAdmin)
admin.site.register(Team)
