from django.shortcuts import render, redirect

from .models import Team, User


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
    return render(request, 'tracker/compare_users.html')
