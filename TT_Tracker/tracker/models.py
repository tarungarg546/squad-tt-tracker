from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.functional import cached_property

from django.contrib.auth.models import User


class Team(models.Model):
    team_name = models.CharField(max_length=30, unique=True, help_text='If Singles, enter same name as user 1 to avoid confusion')
    user_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='firstplayers')
    user_2 = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='secondplayers', help_text='If Singles, leave this empty')

    def __str__(self):
        return self.team_name


class Match(models.Model):
    singles_value = 0
    doubles_value = 1
    CATEGORIES = (
        (singles_value, 'Singles'),
        (doubles_value, 'Doubles'),
    )

    match_name = models.CharField(max_length=62, blank=True, null=True)
    category = models.PositiveSmallIntegerField(choices=CATEGORIES)
    team_1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='firstteams', help_text='Choose team 1 of your category')
    team_2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='secondteams', help_text='Choose team 2 of your category')
    winner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='winners', blank=True, null=True)
    started_at = models.DateTimeField(default=timezone.now)
    ended_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.match_name

    def save(self, *args, **kwargs):
        self.match_name = self.team_1.team_name + 'VS' + self.team_2.team_name
        games_of_match = self.game_set.all()
        total_games = len(games_of_match)
        team_1_wins = len(games_of_match.filter(team_1_score__gt=F('team_2_score')))
        if team_1_wins > total_games/2:
            self.winner = self.team_1
        else:
            self.winner = self.team_2
        super(Match, self).save(*args, **kwargs)

    def clean(self):
        # Raise errors if any one team has 2 users when category is for Singles
        if self.category == '0' and self.team_1.user_2 is not None:
            raise ValidationError(_('team_1 is not for Singles, has two users!'))
        if self.category == '0' and self.team_2.user_2 is not None:
            raise ValidationError(_('team_2 is not for Singles, has two users!'))
        # Raise an error if a user is present in both teams
        if self.category == '0' and self.team_1.user_1 == self.team_2.user_1:
            raise ValidationError(_('User cannot play against himself!'))
        if(self.category == '1' and (self.team_1.user_1 == self.team_2.user_1 or self.team_1.user_1 == self.team_2.user_2 or
           self.team_1.user_2 == self.team_2.user_1 or self.team_1.user_2 == self.team_2.user_2)
           ):
            raise ValidationError(_('One of the users is on both teams!'))
        # Find the winner if winner field is empty
        # self.find_winner()


class Game(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    team_1_score = models.IntegerField(default=0)
    team_2_score = models.IntegerField(default=0)