from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property

from django.contrib.auth.models import User
# Create your models here.


class Team(models.Model):
    team_name = models.CharField(max_length=30, unique=True)
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='firstplayers')
    user2 = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='secondplayers')

    def __str__(self):
        return self.team_name


class Match(models.Model):
    CATEGORIES = (
        ('0', 'Singles'),
        ('1', 'Doubles'),
    )
    category = models.CharField(max_length=1, choices=CATEGORIES)
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='firstteams')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='secondteams')
    winner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='winners')
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField()

    def __str__(self):
        return self.team1.team_name + " vs " + self.team2.team_name

    @cached_property
    def find_winner(self):
        game_set = Game.objects.filter(match=self)
        team1_total = 0
        total_games = 0
        for game in game_set:
            total_games += 1
            if game.team1_score > game.team2_score:
                team1_total += 1
        if team1_total > total_games/2:
            self.winner = self.team1
        else:
            self.winner = self.team2

    @cached_property
    def clean(self):
        # Raise errors if any one team has 2 users when category is for Singles
        if self.category == '0' and self.team1.user2 is not None:
            raise ValidationError(_('team_1 is not for Singles, has two users!'))
        if self.category == '0' and self.team2.user2 is not None:
            raise ValidationError(_('team_2 is not for Singles, has two users!'))
        # Raise an error if a user is present in both teams
        if(self.team1.user1 == self.team2.user1 or self.team1.user1 == self.team2.user2 or
                self.team1.user2 == self.team2.user1 or self.team1.user2 == self.team2.user2
        ):
            raise ValidationError(_('Same user cannot be present in both teams!'))
        # Find the winner if winner field is empty
        if self.winner is None:
            self.find_winner()


class Game(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    team1_score = models.IntegerField(default=0)
    team2_score = models.IntegerField(default=0)