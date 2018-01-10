from django.shortcuts import render, redirect

from .models import Team, User, Match


def index(request):
    user_list = User.objects.all()
    team_list = Team.objects.filter(user_2__isnull=False)
    context = {
        'team_list': team_list,
        'user_list': user_list,
    }
    return render(request, 'tracker/index.html', context)


def compare_teams(request):
    if request.POST['team_1'] == request.POST['team_2']:
        return redirect('tracker:index')
    else:
        post_team_1 = Team.objects.get(id=request.POST['team_1'])
        post_team_2 = Team.objects.get(id=request.POST['team_2'])
        common_matches = (post_team_1.firstteams.filter(team_2=post_team_2)
                          | post_team_1.secondteams.filter(team_1=post_team_2))
        team_1_wins = 0
        team_2_wins = 0
        for match in common_matches:
            if match.winner == post_team_1:
                team_1_wins += 1
            else:
                team_2_wins +=1
        total_matches = team_1_wins + team_2_wins

        if total_matches == 0:
            team_1_win_ratio = 0
            team_2_win_ratio = 0
        else:
            team_1_win_ratio = team_1_wins/total_matches
            team_2_win_ratio = team_2_wins/total_matches
        context = {
            'common_matches': common_matches,
            'total_matches': total_matches,
            'team_1_wins': team_1_wins,
            'team_2_wins': team_2_wins,
            'team_1_win_ratio': team_1_win_ratio,
            'team_2_win_ratio': team_2_win_ratio,
            'team_1': post_team_1,
            'team_2': post_team_2
        }
        return render(request, 'tracker/compare_teams.html', context)


def compare_users(request):
    if request.POST['user_1'] == request.POST['user_2']:
        return redirect('tracker:index')
    else:
        post_user_1 = User.objects.get(id=request.POST['user_1'])
        post_user_2 = User.objects.get(id=request.POST['user_2'])
        all_matches = Match.objects.all()
        user_1_wins = 0
        user_2_wins = 0
        matches_played = 0
        for match in all_matches:
            USER_1_IN_TEAM_1 = match.team_1.user_1 == post_user_1 or match.team_1.user_2 == post_user_1
            USER_1_IN_TEAM_2 = match.team_2.user_1 == post_user_2 or match.team_2.user_2 == post_user_2
            USER_2_IN_TEAM_1 = match.team_1.user_1 == post_user_2 or match.team_1.user_2 == post_user_2
            USER_2_IN_TEAM_2 = match.team_2.user_1 == post_user_1 or match.team_2.user_2 == post_user_1

            if (
                    (USER_1_IN_TEAM_1 and USER_2_IN_TEAM_2) or (USER_1_IN_TEAM_2 and USER_2_IN_TEAM_1)):
                matches_played += 1
                if USER_1_IN_TEAM_1 and match.winner == match.team_1:
                    user_1_wins += 1
                else:
                    user_2_wins += 1
        if matches_played == 0:
            user_1_win_ratio = 0
            user_2_win_ratio = 0
        else:
            user_1_win_ratio = user_1_wins/matches_played
            user_2_win_ratio = user_2_wins/matches_played
        context = {
            'user_1': post_user_1,
            'user_2': post_user_2,
            'matches_played': matches_played,
            'user_1_wins': user_1_wins,
            'user_2_wins': user_2_wins,
            'user_1_win_ratio': user_1_win_ratio,
            'user_2_win_ratio': user_2_win_ratio,
        }
        return render(request, 'tracker/compare_users.html', context)
