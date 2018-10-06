# For running this custom command use python manage.py import_csv_data matches /home/dell/PycharmProjects/data_project1/data/matches.csv
# For running this custom command use python manage.py import_csv_data deliveries /home/dell/PycharmProjects/data_project1/data/deliveries.csv
from django.core.management.base import BaseCommand
from data_project.models import Matches, Deliveries
import csv


def import_csv_to_database(class_name, file_url):
    lst_of_objects = []
    if class_name == 'matches':
        with open(file_url, 'r') as file_handle:
            for match in csv.DictReader(file_handle):
                match_obj = Matches(
                    season = match['season'],
                    city = match['city'],
                    date = match['date'],
                    team1 = match['team1'],
                    team2 = match['team2'],
                    toss_winner = match['toss_winner'],
                    toss_decision = match['toss_decision'],
                    result = match['result'],
                    dl_applied = match['dl_applied'],
                    winner = match['winner'],
                    win_by_runs = match['win_by_runs'],
                    win_by_wickets = match['win_by_wickets'],
                    player_of_match = match['player_of_match'],
                    venue = match['venue'],
                    umpire1 = match['umpire1'],
                    umpire2 = match['umpire2'],
                    umpire3 = match['umpire3']
                )
                lst_of_objects.append(match_obj)
        Matches.objects.bulk_create(lst_of_objects)
        return True
    elif class_name == 'deliveries':
        with open(file_url, 'r') as file_handle:
            for delivery in csv.DictReader(file_handle):
                delivery_obj = Deliveries(
                    match_id = Matches.objects.get(pk=delivery['match_id']),
                    inning = delivery['inning'],
                    batting_team = delivery['batting_team'],
                    bowling_team = delivery['bowling_team'],
                    over = delivery['over'],
                    ball = delivery['ball'],
                    batsman = delivery['batsman'],
                    non_striker = delivery['non_striker'],
                    bowler = delivery['bowler'],
                    is_super_over = delivery['is_super_over'],
                    wide_runs = delivery['wide_runs'],
                    bye_runs = delivery['bye_runs'],
                    legbye_runs = delivery['legbye_runs'],
                    noball_runs = delivery['noball_runs'],
                    penalty_runs = delivery['penalty_runs'],
                    batsman_runs = delivery['batsman_runs'],
                    extra_runs = delivery['extra_runs'],
                    total_runs = delivery['total_runs'],
                    player_dismissed = delivery['player_dismissed'],
                    dismissal_kind = delivery['dismissal_kind'],
                    fielder = delivery['fielder']
                )
                lst_of_objects.append(delivery_obj)
        Deliveries.objects.bulk_create(lst_of_objects)
        return True
    else:
        return False


class Command(BaseCommand):
    help = 'Imports CSV data to a pre-defined table'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Model name for data insertion')
        parser.add_argument('url', type=str, help='File location of CSV')
        # parser.add_argument('-y', '--first_col', action='store_true', help='Enter this flag to include first column from csv')

    def handle(self, *args, **options):
        class_name = options['name']
        file_path = options['url']
        record_creation_status = import_csv_to_database(class_name, file_path)
        if record_creation_status:
            self.stdout.write(f"All records for {class_name} has been inserted into database")
        else:
            self.stdout.write("Please check your class name speelings")
