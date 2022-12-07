#!/usr/bin/python


#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
#__imports__
import json
import time
import requests
import os
import basketball_reference_scraper.teams as brs_t
import basketball_reference_scraper.players as brs_p
import basketball_reference_scraper.seasons as brs_s
import basketball_reference_scraper.box_scores as brs_bs
import basketball_reference_scraper.pbp as brs_pbp
import basketball_reference_scraper.shot_charts as brs_sc
from collections import namedtuple
#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
#__init__
team_list = ['ATL', 'BRK','BOS', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'TOR', 'UTA', 'WAS'] 
key = {'ATL':'AtlantaHawks', 'BRK':'BrooklynNets', 'BOS':'BostonCeltics', 'CHA':'CharlotteHornets','CHI':'ChicagoBulls','CLE':'ClevelandCavaliers','DAL':'DallasMavericks','DEN':'DenverNuggets','DET':'DetroitPistons',
           'GSW':'GoldenStateWarriors','HOU':'HoustonRockets','IND':'IndianaPacers','LAC':'LosAngelesClippers','LAL':'LosAngelesLakers','MEM':'MemphisGrizzlies','MIA':'MiamiHeat','MIL':'MilwaukeeBucks','MIN':'MinnesotaTimberwolves',
           'NOP':'NewOrleansPelicans','NYK':'NewYorkKnicks','OKC':'OklahomaCityThunder','ORL':'OrlandoMagic','PHI':'Philadelphia76ers','PHO':'PhoenixSuns','POR':'PortlandTrailBlazers','SAC':'SacramentoKings','TOR':'TorontoRaptors',
           'UTA':'UtahJazz','WAS':'WashingtonWizards'}
count = 0
t = time.localtime()
current_date = time.strftime("%D",t)
current_date = str('20' + current_date[6:8] + '-' + current_date[0:2] + '-' + current_date[3:5])
script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)


#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
#__url's__and__urlprocessor__
start_json = 'http://data.nba.net/10s/prod/v1/today.json'
nba_teams = 'http://data.nba.net/prod/v2/2022/teams.json'
def json(URL):
    resp = requests.get(URL)
    resp = resp.json()
    return resp
#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
#__basketballreferencetools__

'''
date format: YYYY-MM-DD
brs_t          --- get_roster(team,season)
                  --- get_team_stats(team, season_end_year, data_format='PER_GAME')
                  --- get_opp_stats(team, season_end_year, data_format='PER_GAME')
                  --- get_roster_stats(team, season, data_format='PER_GAME', playoffs=False)
                  --- get_team_misc(team, season)
                  
brs_p         --- get_stats(name, stat_type='PER_GAME', playoffs=False, career=False)
                  --- get_game_logs(name, start_date, end_date, playoffs=False)

brs_s          --- get_schedule(season, playoffs=False)
                  --- get_standings(date=None)
                  
brs_bs       --- get_box_scores(date, team1, team2, period='GAME|Q1|Q2|Q3|Q4|H1|H2, stat_type='BASIC|ADVANCED')
brs_pbp     --- get_pbp(date,team1,team2)

brs_sc        --- get_shot_chart(date, team1,team2)

'''

