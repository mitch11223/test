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
import pandas
import numpy
import html5lib
import logtester
#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
#__init__
team_list = ['ATL',
             'BOS',
             'BRK',
             'CHO',
             'CHI',
             'CLE',
             'DAL',
             'DEN',
             'DET',
             'GSW',
             'HOU',
             'IND',
             'LAC',
             'LAL',
             'MEM',
             'MIA',
             'MIL',
             'MIN',
             'NOP',
             'NYK',
             'OKC',
             'ORL',
             'PHI',
             'PHO',
             'POR',
             'SAC',
             'SAS',
             'TOR',
             'UTA',
             'WAS'] 
key = {'ATL':'AtlantaHawks', 'BOS':'BostonCeltics', 'BRK':'BrooklynNets','CHO':'CharlotteHornets','CHI':'ChicagoBulls','CLE':'ClevelandCavaliers','DAL':'DallasMavericks','DEN':'DenverNuggets','DET':'DetroitPistons',
           'GSW':'GoldenStateWarriors','HOU':'HoustonRockets','IND':'IndianaPacers','LAC':'LosAngelesClippers','LAL':'LosAngelesLakers','MEM':'MemphisGrizzlies','MIA':'MiamiHeat','MIL':'MilwaukeeBucks','MIN':'MinnesotaTimberwolves',
           'NOP':'NewOrleansPelicans','NYK':'NewYorkKnicks','OKC':'OklahomaCityThunder','ORL':'OrlandoMagic','PHI':'Philadelphia76ers','PHO':'PhoenixSuns','POR':'PortlandTrailBlazers','SAC':'SacramentoKings','SAS':'SanAntonioSpurs','TOR':'TorontoRaptors',
           'UTA':'UtahJazz','WAS':'WashingtonWizards'}
key_2 = {value: key for key, value in key.items()}

date_list = []
home_list = []
away_list = []
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


league_schedule = pandas.read_csv('TeamFiles/League/Schedule/Full_Schedule.txt')

class box_scores:
    def __init__(self, date, away_team, home_team, period='GAME', stat_type='BASIC'):
        self.date = date
        self.away_team = away_team
        self.home_team = home_team
        self.period = period
        self.stat_type = stat_type
    def acquire_box_score(self):
        box_score = brs_bs.get_box_scores(self.date,self.away_team,self.home_team,self.period,self.stat_type)
        return box_score
    



def process_lists_and_files():
    
    date = league_schedule['Date']
    for day in date:
        date_list.append(day)
    away_team = league_schedule['Visitor/Neutral']
    for team in away_team:
        away_list.append(team)
    home_team = league_schedule['Home/Neutral']
    for team in home_team:
        home_list.append(team)
            
    
    
    for i in range(len(league_schedule)):
        #assign date, away and home teams as variables
        date = date_list[i]
        away = away_list[i]
        home = home_list[i]
        away_team = away_list[i]
        home_team = home_list[i]
        #convert teams from full to abbreviations
        away = key_2[away]
        home = key_2[home]
        #filename creation to parse
        away_filename = str('TeamFiles/' + away_team + '/Boxscores/' + date + '/' + away_team + 'box_score.txt')
        home_filename = str('TeamFiles/' + home_team + '/Boxscores/' + date + '/' + home_team + 'box_score.txt')
        away_opponent = str('TeamFiles/' + away_team + '/Boxscores/' + date + '/' + home_team + 'box_score.txt')
        home_opponent = str('TeamFiles/' + home_team + '/Boxscores/' + date + '/' + away_team + 'box_score.txt')
        
        #check if files exists
        if os.path.exists(away_filename) and os.path.exists(home_filename) and os.path.exists(away_opponent) and os.path.exists(home_opponent) == True:
            print(date, away, home)
            print('Files already exists...Bypassing')
            
        else:
            os.makedirs(os.path.dirname(away_filename), exist_ok=True)
            os.makedirs(os.path.dirname(home_filename), exist_ok=True)
            os.makedirs(os.path.dirname(away_opponent), exist_ok=True)
            os.makedirs(os.path.dirname(home_opponent), exist_ok=True)
            
            #EXECUTE THIS IF PATH HAS NOT ALREADY BEEN MADE
            time.sleep(5)
            print(date, away, home)
            game = box_scores(date,away,home)
            try:
                box_score_results = game.acquire_box_score()
                away_box_score = box_score_results[away]
                home_box_score = box_score_results[home]
                away_box_score = away_box_score.to_csv(index=False)
                home_box_score = home_box_score.to_csv(index=False)
                
                away_file = open(away_filename, 'a+')
                away_file.write(away_box_score)        
                away_file.close()
                
                away_opponent_file = open(away_opponent, 'a+')
                away_opponent_file.write(home_box_score)
                away_opponent_file.close()
                print('Away Game Log Added')

                
                home_file = open(home_filename, 'a+')
                home_file.write(home_box_score)
                home_file.close()
                
                home_opponent_file = open(home_opponent, 'a+')
                home_opponent_file.write(away_box_score)
                home_opponent_file.close()
                print('Home Game Log Added')
                
            except AttributeError:
                print('Attribute Error...Game Skipped')
                break
            except ValueError:
                print('Value Error...Game Skipped')
        













'/Users/kingmitch/Library/Python/3.7/lib/python/site-packages/nba_api/live/nba'

  
    
    
import nba_api.stats.endpoints as stats_endpoints
import nba_api.live.nba.endpoints as today_endpoints
import pandas



teamIDkey = {'ATL':'1610612737','BRK':'1610612751','BOS':'1610612738','CHO':'1610612766','CLE':'1610612739',
             'CHI':'1610612741', 'DAL':'1610612742', 'DEN':'1610612743', 'DET':'1610612765', 'GSW':'1610612744',
             'HOU':'1610612745', 'IND':'1610612754', 'LAC':'1610612746','LAL':'1610612747','MEM':'1610612763',
             'MIA':'1610612748', 'MIL':'1610612749', 'MIN':'1610612750', 'NYK':'1610612752', 'NOP':'1610612740',
             'OKC':'1610612760', 'ORL':'1610612753', 'PHI':'1610612755', 'PHO':'1610612756','POR':'1610612757',
             'SAS':'1610612759', 'SAC':'1610612758', 'TOR':'1610612761','UTA':'1610612762','WAS':'1610612764'}

teamIDkey_2 = {value: key for key, value in teamIDkey.items()}
#returns each quarter's points for both teams
def Quarter_Points(gameID,team):
    if team == 'BRK':
        team = 'BKN'
    elif team == 'CHO':
        team = 'CHA'
    elif team == 'PHO':
        team = 'PHX'
    
    
    
    #to get home/away team
    BoxScoreSummary = stats_endpoints.boxscoresummaryv2.BoxScoreSummaryV2(gameID)
    BoxScoreSummary = BoxScoreSummary.get_dict()
    BoxScoreSummary = BoxScoreSummary['resultSets']
    GameSummary = BoxScoreSummary[0]
    GameSummary = GameSummary['rowSet']
    GameSummary = GameSummary[0]
    HomeID = GameSummary[6]
    HomeID = str(HomeID)
    HomeTeam = teamIDkey_2[HomeID]
    if HomeTeam == 'BRK':
        HomeTeam = 'BKN'
    elif HomeTeam == 'CHO':
        HomeTeam = 'CHA'
    elif HomeTeam == 'PHO':
        HomeTeam = 'PHX'
    
    
    
    BoxScoreSummary = BoxScoreSummary[5]
    headers = BoxScoreSummary['headers']
    data = BoxScoreSummary['rowSet']
    df = pandas.DataFrame(data, columns = headers)
    #grab only one date
    date = df["GAME_DATE_EST"]
    
    
    
    
    
    #optional to create
    new = df[['TEAM_ABBREVIATION','PTS_QTR1','PTS_QTR2','PTS_QTR3','PTS_QTR4']]
    if HomeTeam == team:
        loc = 'H'
    else:
        loc = 'A'
    
    teamdf = new.loc[new['TEAM_ABBREVIATION'] == team]
    oppdf = new.loc[new['TEAM_ABBREVIATION'] != team]
    opp = oppdf['TEAM_ABBREVIATION'].to_list()
    opp = opp[0]
    
    
    #variable per value(team opponent scores etc...)
    

    date = date[0]
    teamq1 = teamdf['PTS_QTR1'].to_list()
    oppq1 = oppdf['PTS_QTR1'].to_list()
    teamq2 = teamdf['PTS_QTR2'].to_list()
    oppq2 = oppdf['PTS_QTR2'].to_list()
    teamq3 = teamdf['PTS_QTR3'].to_list()
    oppq3 = oppdf['PTS_QTR3'].to_list()
    teamq4 = teamdf['PTS_QTR4'].to_list()
    oppq4 = oppdf['PTS_QTR4'].to_list()
    teamq1 = teamq1[0]
    oppq1 = oppq1[0]
    teamq2 = teamq2[0]
    oppq2 = oppq2[0]
    teamq3 = teamq3[0]
    oppq3 = oppq3[0]
    teamq4 = teamq4[0]
    oppq4 = oppq4[0]
    margq1 = teamq1 - oppq1
    totq1 = teamq1 + oppq1
    margq2 = teamq2 - oppq2
    totq2 = teamq2 + oppq2
    margq3 = teamq3 - oppq3
    totq3 = teamq3 + oppq3
    margq4 = teamq4 - oppq4
    totq4 = teamq4 + oppq4
    
    
    
    teamh1pts = teamq1 + teamq2
    teamh2pts = teamq3 + teamq4
    opph1pts = oppq1 + oppq2
    opph2pts = oppq3 + oppq4
    
    h1margin = teamh1pts - opph1pts
    h2margin = teamh2pts - opph2pts
    h1total = teamh1pts + opph1pts
    h2total = teamh2pts + opph2pts
    teampts = teamh1pts + teamh2pts
    opppts = opph1pts + opph2pts
    gamemargin = teampts - opppts
    gametotal = teampts + opppts
    
    if teampts > opppts:
        game_wl = 1
    elif teampts < opppts:
        game_wl = -1
    else:
        game_wl = 0
    
    
    #calculate if game was won or lost
    
    
    
    
    #calculate if half was won or lost
    if teamh1pts > opph1pts:
        h1wl = 1
    elif teamh1pts < opph1pts:
        h1wl = -1
    else:
        h1wl = 0
    
    if teamh2pts > opph2pts:
        h2wl = 1
    elif teamh2pts < opph2pts:
        h2wl = -1
    else:
        h2wl = 0
    
    
    #calculate if quarter was won or lost
    if (teamq1 - oppq1) > 0:
        wlq1 = 1
    elif (teamq1 - oppq1) < 0:
        wlq1 = -1
    else:
        wlq1 = 0
        
    if (teamq2 - oppq2) > 0:
        wlq2 = 1
    elif (teamq2 - oppq2) < 0:
        wlq2 = -1
    else:
        wlq2 = 0
        
    if (teamq3 - oppq3) > 0:
        wlq3 = 1
    elif (teamq3 - oppq3) < 0:
        wlq3 = -1
    else:
        wlq3 = 0
        
    if (teamq4 - oppq4) > 0:
        wlq4 = 1
    elif (teamq4 - oppq4) < 0:
        wlq4 = -1
    else:
        wlq4 = 0
    
    
    
    
    if team == 'BKN':
        team = 'BRK'
    elif team == 'CHA':
        team = 'CHO'
    elif team == 'PHX':
        team = 'PHO'
    q_key = {'Team':team,'Opp':opp,'Location':loc,'Date':date[:10],'Q1':[teamq1,oppq1,margq1,wlq1,totq1],'Q2':[teamq2,oppq2,margq2,wlq2,totq2,teamh1pts,opph1pts,h1margin,h1total,h1wl],'Q3':[teamq3,oppq3,margq3,wlq3,totq3],'Q4':[teamq4,oppq4,margq4,wlq4,totq4,teamh2pts,opph2pts,h2margin,h2total,h2wl,teampts,opppts,gamemargin,gametotal,game_wl]}
    
    
    print(q_key)
    return q_key
    
    



#gets list of all valid game id's for a team this season
def get_gameid(teamID):
    log = stats_endpoints.teamgamelogs.TeamGameLogs(team_id_nullable = teamID, season_nullable = '2022-23')
    log = log.get_dict()
    log = log['resultSets']
    log = log[0]
    headers = log['headers']
    data = log['rowSet']
    df = pandas.DataFrame(data,columns = headers)
    game_IDs = df['GAME_ID'].to_list()
    return game_IDs


def write_q_logs():
    q_list = ['Q1','Q2','Q3','Q4']
    #inputs every game id per team and pulls out the quarter by quarter points
    leaguequarterfilename = str('TeamFiles/League/Quarters/LeagueQuarterFile.txt')
    os.makedirs(os.path.dirname(leaguequarterfilename), exist_ok=True)
    leaguequarterfile = open(leaguequarterfilename,'w+')
    leaguequarterfile.write('Team,Opp,Location,Date,Q1_for,Q1_against,Q1_margin,Q1_WL,Q1_total,Q2_for,Q2_against,Q2_margin,Q2_WL,Q2_total,H1_for,H1_against,H1_margin,H1_total,H1_WL,Q3_for,Q3_against,Q3_margin,Q3_WL,Q3_total,Q4_for,Q4_against,Q4_margin,Q4_WL,Q4_total,H2_for,H2_against,H2_margin,H2_total,H2_WL,G_For,G_against,G_margin,G_total,G_WL' + '\n')
    
    
    #Spread_DF = pandas.read_csv('TeamFiles/League/Schedule/SpreadDay.txt')
    
    for team in team_list:
        teamqfile = str('TeamFiles/' + key[team] + '/Quarters/Quarter_File.txt')
        print(teamqfile)
        os.makedirs(os.path.dirname(teamqfile), exist_ok=True)
        teamIDlist = get_gameid(teamIDkey[team])
        print('Executing:',team)
        q_file = open(teamqfile,'w+')
        q_file.write('Team,Opp,Location,Date,Q1_for,Q1_against,Q1_margin,Q1_WL,Q1_total,Q2_for,Q2_against,Q2_margin,Q2_WL,Q2_total,H1_for,H1,against,H1_margin,H1_total,H1_WL,Q3_for,Q3_against,Q3_margin,Q3_WL,Q3_total,Q4_for,Q4_against,Q4_margin,Q4_WL,Q4_total,H2_for,H2_against,H2_margin,H2_total,H2_WL,G_For,G_against,G_margin,G_total,G_WL' + '\n')
        for game in teamIDlist:
            log = Quarter_Points(game,team)
            #/Team/Quarters/Quarterfile.txt
            #organized by game (g1 [INSERT ALL QUARTER DATA HERE]..q2...q3...q4,
            #                   g2 [INSERT ALL QUARTER DATA HERE]..q2...q3...q4 )
            logtowrite = []
            opponent = log['Opp']
            date = log['Date']
            location = log['Location']
            
            
            leaguequarterfile.write(team + ',' + opponent + ',' + location + ',' + date)
            q_file.write(team + ',' + opponent + ',' + location + ',' + date)
            for quarter in q_list:
                info = log[quarter]
                for item in info:
                    logtowrite.append(str(item))
            for item in logtowrite:
                q_file.write(',' + item)
                leaguequarterfile.write(',' + item)
                
            
            q_file.write('\n')
            leaguequarterfile.write('\n')
        q_file.close()
    leaguequarterfile.close()















def execute():
    print('Initiating all_time Class')
    #all_time = logtester.all_time()
    print('Executing Cleaning the glass DataLog...This will take a few minutes')
    #all_time.cleaning_the_glass()
    print('Executing file processing...')
    #process_lists_and_files()
    print('Writing team quarter logs...')
    write_q_logs()
execute()