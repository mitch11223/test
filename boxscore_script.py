#!/usr/bin/python
import json
import time
import requests
import os,glob
import basketball_reference_scraper.teams as brs_t
import basketball_reference_scraper.players as brs_p
import basketball_reference_scraper.seasons as brs_s
import basketball_reference_scraper.box_scores as brs_bs
import pandas
import numpy


#__init__
abbreviation_list = ['ATL', 'BRK','BOS', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'TOR', 'UTA', 'WAS'] 
key = {'ATL':'AtlantaHawks', 'BRK':'BrooklynNets', 'BOS':'BostonCeltics', 'CHA':'CharlotteHornets','CHI':'ChicagoBulls','CLE':'ClevelandCavaliers','DAL':'DallasMavericks','DEN':'DenverNuggets','DET':'DetroitPistons',
           'GSW':'GoldenStateWarriors','HOU':'HoustonRockets','IND':'IndianaPacers','LAC':'LosAngelesClippers','LAL':'LosAngelesLakers','MEM':'MemphisGrizzlies','MIA':'MiamiHeat','MIL':'MilwaukeeBucks','MIN':'MinnesotaTimberwolves',
           'NOP':'NewOrleansPelicans','NYK':'NewYorkKnicks','OKC':'OklahomaCityThunder','ORL':'OrlandoMagic','PHI':'Philadelphia76ers','PHO':'PhoenixSuns','POR':'PortlandTrailBlazers','SAC':'SacramentoKings','TOR':'TorontoRaptors',
           'UTA':'UtahJazz','WAS':'WashingtonWizards'}
league_schedule = pandas.read_csv('TeamFiles/League/Schedule/Full_Schedule.txt')
#print(league_schedule)
#Contains all full team names
team_list = []

count = 0
t = time.localtime()
current_date = time.strftime("%D",t)
current_date = str('20' + current_date[6:8] + '-' + current_date[0:2] + '-' + current_date[3:5])
script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)
#-------------------------


#-------------------------


#create team list

    
#A class that is initialized per team essentially to grab all game days and put in a dataframe
class Schedules:
    def __init__(self,team):
        self.team = team
    def compute_schedule(self):
        away_games = league_schedule.loc[league_schedule['Visitor/Neutral'] == self.team]
        home_games = league_schedule.loc[league_schedule['Home/Neutral'] == self.team]
        all_games = away_games.append(home_games)
        all_games = all_games.sort_values(by=['Date'])
        #returns dataframe of all teams games
        return all_games['Date']


#this function can pull game logs frm every game day
def TeamFilesSchedule(TeamName):
    game_dates = []
    team_schedule = Schedules(TeamName)
    #dataframe of all teams games
    team_schedule = team_schedule.compute_schedule()
    for date in team_schedule:
        filename = str(TeamName + 'box_score.txt')
        os.chdir(script_dir)
        directory = str('TeamFiles/' + TeamName + '/')
        game_dates.append(date)
        directory = str(directory + date)
        #Directory is the directory per game day
        


'''
for value in key:
    team_list.append(key[value])
'''    
#pull specific game logs through directories matching criteria


TeamFilesSchedule('AtlantaHawks')  