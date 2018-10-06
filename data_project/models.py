import datetime
from django.db import models
from django.utils import timezone


class Matches(models.Model):
    season = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    date = models.DateTimeField('Date')
    team1 = models.CharField(max_length=200)
    team2 = models.CharField(max_length=200)
    toss_winner = models.CharField(max_length=200)
    toss_decision = models.CharField(max_length=200)
    result = models.CharField(max_length=200)
    dl_applied = models.IntegerField(default=0)
    winner = models.CharField(max_length=200)
    win_by_runs = models.IntegerField(default=0)
    win_by_wickets = models.IntegerField(default=0)
    player_of_match = models.CharField(max_length=200)
    venue = models.CharField(max_length=200)
    umpire1 = models.CharField(max_length=200)
    umpire2 = models.CharField(max_length=200)
    umpire3 = models.CharField(max_length=200)

    def __str__(self):
        return f"Matches({self.id}, {self.season}, {self.city}, {self.date}, {self.team1}, {self.team2}, {self.winner})"


class Deliveries(models.Model):
    match_id = models.ForeignKey(Matches, on_delete=models.CASCADE)
    inning = models.IntegerField(default=0)
    batting_team = models.CharField(max_length=200)
    bowling_team = models.CharField(max_length=200)
    over = models.IntegerField(default=0)
    ball = models.IntegerField(default=0)
    batsman = models.CharField(max_length=200)
    non_striker = models.CharField(max_length=200)
    bowler = models.CharField(max_length=200)
    is_super_over = models.IntegerField(default=0)
    wide_runs = models.IntegerField(default=0)
    bye_runs = models.IntegerField(default=0)
    legbye_runs = models.IntegerField(default=0)
    noball_runs = models.IntegerField(default=0)
    penalty_runs = models.IntegerField(default=0)
    batsman_runs = models.IntegerField(default=0)
    extra_runs = models.IntegerField(default=0)
    total_runs = models.IntegerField(default=0)
    player_dismissed = models.CharField(max_length=200)
    dismissal_kind = models.CharField(max_length=200)
    fielder = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.bowler} is bowling in match for season {self.match_id.season}"

    # def was_published_recently(self):
    #     return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
