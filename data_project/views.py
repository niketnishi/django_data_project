from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import loader
from .models import Matches, Deliveries
from django.db.models import Count, Sum
from collections import OrderedDict
import json


def index(request):
    return render(request, 'data_project/index.html')

# Plot the number of matches played per year of all the years in IPL.
# annotate is used to create new fields


def num_of_match_each_year(request):
    data_dict = OrderedDict()
    result = Matches.objects.values('season').annotate(season_count=Count("season"))
    for item in result:
        if item['season'] not in data_dict:
            data_dict[item['season']] = item['season_count']

    template = loader.get_template('data_project/first_question.html')
    context = {
        'season': json.dumps(list(data_dict.keys())),
        'frequency': json.dumps(list(data_dict.values()))
    }
    # print(f"{data_dict}")
    return HttpResponse(template.render(context, request))

# Plot a stacked bar chart of matches won of all teams over all the years of IPL.


def matches_won_by_team(data_dict, lst_of_winning_team):    # Returns the matches won per team in year 2008 to 2017
    matches_per_team = {}

    for team in lst_of_winning_team:
        matches_per_team[team] = []

    for season in data_dict:
        for team in data_dict[season]:
            matches_per_team[team].append(data_dict[season][team])

        for team in lst_of_winning_team:        # Inserting zero for the team which is not won in a season
            if team not in data_dict[season]:
                matches_per_team[team].append(0)
    return matches_per_team


def stacked_bar_chart(request):
    data_dict, lst_of_winning_team = {}, []
    result = Matches.objects.values('season', 'winner').annotate(win_count=Count("winner"))
    for item in result:
        if item['season'] not in data_dict:
            data_dict[item['season']] = {}
        if item['winner'] != "":
            if item['winner'] not in data_dict[item['season']]:
                data_dict[item['season']][item['winner']] = 0
            if item['winner'] not in lst_of_winning_team:
                lst_of_winning_team.append(item['winner'])
            data_dict[item['season']][item['winner']] += int(item['win_count'])
    matches_won = matches_won_by_team(data_dict, lst_of_winning_team)
    template = loader.get_template('data_project/second_question.html')
    context = {
        'lst_of_season': json.dumps(list(data_dict.keys())),
        'matches_won': matches_won
    }
    # print(f"{data_dict}")
    return HttpResponse(template.render(context, request))

# For the year 2016 plot the extra runs conceded per team.


def match_2016_extra_run(request):
    data_dict, lst_of_id = OrderedDict(), []

    match_obj = Matches.objects.values('id').filter(season='2016')
    for item in match_obj:
        lst_of_id.append(item['id'])

    result = Deliveries.objects.filter(match_id__in=lst_of_id).values('bowling_team').annotate(ext_runs=Sum("extra_runs"))
    for item in result:
        if item['bowling_team'] not in data_dict:
            data_dict[item['bowling_team']] = item['ext_runs']

    template = loader.get_template('data_project/third_question.html')
    context = {
        'lst_of_team': json.dumps(list(data_dict.keys())),
        'lst_of_extra_runs': json.dumps(list(data_dict.values()))
    }
    # print(f"{data_dict}")
    return HttpResponse(template.render(context, request))

# For the year 2015 plot the top economical bowlers.


def match_2015_eco_bowler(request):
    eco_bowler, lst_of_id = {}, []

    match_obj = Matches.objects.values('id').filter(season='2015')
    for item in match_obj:
        lst_of_id.append(item['id'])

    result = Deliveries.objects.filter(match_id__in=lst_of_id).values('bowler').annotate(tot_runs=Sum("total_runs")).annotate(no_of_balls=Count("over"))
    for item in result:
        if item['bowler'] not in eco_bowler:
            eco_bowler[item['bowler']] = round(item['tot_runs'] * 6 / item['no_of_balls'], 1)

    template = loader.get_template('data_project/fourth_question.html')
    eco_bowler = OrderedDict(sorted(eco_bowler.items(), key=lambda x: x[1])[:10])
    context = {
        'bowler': json.dumps(list(eco_bowler.keys())),
        'eco_rate': json.dumps(list(eco_bowler.values()))
    }
    # print(f"{eco_bowler}")
    return HttpResponse(template.render(context, request))

# Match summary for players winning man of the match maximum number of times in a given year.


def match_summary_over_years(request):
    data_dict = {}
    result = Matches.objects.values('player_of_match').filter(season='2017').annotate(frequency=Count('player_of_match'))
    for item in result:
        if item['player_of_match'] not in data_dict:
            data_dict[item['player_of_match']] = item['frequency']
    data_dict = OrderedDict(sorted(data_dict.items(), key=lambda x: x[1], reverse=True)[:10])
    template = loader.get_template('data_project/fifth_question.html')
    context = {
        'player_of_match': json.dumps(list(data_dict.keys())),
        'frequency': json.dumps(list(data_dict.values()))
    }
    # print(f"{data_dict}")
    return HttpResponse(template.render(context, request))
