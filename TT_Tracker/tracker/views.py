from __future__ import division

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Case, When, IntegerField, Q, Value
from django.db.models.functions import Coalesce

from .models import Team, User, Match


@login_required
def index(request):
    user_list = User.objects.all()
    team_list = Team.objects.filter(user_2__isnull=False)
    context = {
        'team_list': team_list,
        'user_list': user_list,
    }
    return render(request, 'tracker/index.html', context)


@login_required
def compare_teams(request):
    # Redirect back if teams entered are same
    if request.POST['team_1'] == request.POST['team_2'] or request.POST['team_1'] is None or request.POST['team_2'] is None:
        return redirect('tracker:index')
    # Get the two Team objects required through their id
    post_team_list = Team.objects.filter(id__in=(request.POST['team_1'], request.POST['team_2']))
    if post_team_list[0].id == request.POST['team_1']:
        post_team_1 = post_team_list[0]
        post_team_2 = post_team_list[1]
    else:
        post_team_1 = post_team_list[1]
        post_team_2 = post_team_list[0]
    common_matches = (post_team_1.firstteams.filter(team_2=post_team_2)
                      | post_team_1.secondteams.filter(team_1=post_team_2))
    # Aggregate wins of both teams
    win_dict = common_matches.aggregate(
        team_1_wins=Coalesce(Sum(
            Case(When(winner=post_team_1, then=1), output_field=IntegerField())
        ), Value(0)),
        team_2_wins=Coalesce(Sum(
           Case(When(winner=post_team_2, then=1), output_field=IntegerField())
        ), Value(0))
    )

    total_matches = win_dict['team_1_wins'] + win_dict['team_2_wins']
    if total_matches == 0:
        team_1_win_ratio = 0
        team_2_win_ratio = 0
    else:
        team_1_win_ratio = win_dict['team_1_wins']/total_matches
        team_2_win_ratio = win_dict['team_2_wins']/total_matches
    context = {
        'common_matches': common_matches,
        'total_matches': total_matches,
        'team_1_win_ratio': team_1_win_ratio,
        'team_2_win_ratio': team_2_win_ratio,
        'team_1': post_team_1,
        'team_2': post_team_2
    }
    context.update(win_dict)
    return render(request, 'tracker/compare_teams.html', context)


@login_required
def compare_users(request):
    # Redirect back if users entered are same or none
    if request.POST['user_1'] == request.POST['user_2'] or request.POST['user_1'] is None or request.POST['user_2'] is None:
        return redirect('tracker:index')
    # Get the two User objects required from their id
    post_user_list = User.objects.filter(id__in=(request.POST['user_1'], request.POST['user_2']))
    if post_user_list[0].id == request.POST['user_1']:
        post_user_1 = post_user_list[0]
        post_user_2 = post_user_list[1]
    else:
        post_user_1 = post_user_list[1]
        post_user_2 = post_user_list[0]

    common_matches = Match.objects.filter((Q(team_1__user_1=post_user_1) | Q(team_1__user_2=post_user_1))
                                          & (Q(team_2__user_1=post_user_2) | Q(team_2__user_2=post_user_2))
                                          | (Q(team_2__user_1=post_user_1) | Q(team_2__user_2=post_user_1))
                                          & (Q(team_1__user_1=post_user_2) | Q(team_1__user_2=post_user_2)))

    played_dict = common_matches.aggregate(
        user_1_wins=Coalesce(Sum(
            Case(When(winner__user_1=post_user_1, then=1),
                 When(winner__user_2=post_user_1, then=1),
                 output_field=IntegerField())
        ), Value(0)),
        user_2_wins=Coalesce(Sum(
            Case(When(winner__user_1=post_user_2, then=1),
                 When(winner__user_2=post_user_2, then=1),
                 output_field=IntegerField())
        ), Value(0))
    )

    matches_played = played_dict['user_1_wins'] + played_dict['user_2_wins']
    if matches_played == 0:
        user_1_win_ratio = 0
        user_2_win_ratio = 0
    else:
        user_1_win_ratio = float(played_dict['user_1_wins'])/float(matches_played)
        user_2_win_ratio = float(played_dict['user_2_wins'])/float(matches_played)
    context = {
        'user_1': post_user_1,
        'user_2': post_user_2,
        'matches_played': matches_played,
        'user_1_win_ratio': user_1_win_ratio,
        'user_2_win_ratio': user_2_win_ratio,
        'common_matches': common_matches,
    }
    context.update(played_dict)
    return render(request, 'tracker/compare_users.html', context)
