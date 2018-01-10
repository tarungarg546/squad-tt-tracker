from django.shortcuts import render, redirect

from .models import Team


def index(request):
    team_list = Team.objects.all()
    context = {'team_list': team_list}
    return render(request, 'tracker/index.html', context)

def compare(request):
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
        return render(request, 'tracker/compare.html', context)
