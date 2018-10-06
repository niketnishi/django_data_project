from django.urls import path
from . import views

app_name = 'data_project'
urlpatterns = [
    path('', views.index, name='index'),
    path('data_project/first_question/', views.num_of_match_each_year, name='num_of_match_each_year'),
    path('data_project/second_question/', views.stacked_bar_chart, name='stacked_bar_chart'),
    path('data_project/third_question/', views.match_2016_extra_run, name='match_2016_extra_run'),
    path('data_project/fourth_question/', views.match_2015_eco_bowler, name='match_2015_eco_bowler'),
    path('data_project/fifth_question/', views.match_summary_over_years, name='match_summary_over_years'),
]
