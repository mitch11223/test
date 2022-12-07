#!/usr/bin/python
import json
import time
import requests
import os


#Start
#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
game_list = []
team_list = {}
count = 0
t = time.localtime()
date = time.strftime("%D",t)
current_date = str('20' + date[6:8] + '-' + date[0:2] + '-' + date[3:5])
script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)




start_json = 'http://data.nba.net/10s/prod/v1/today.json'
nba_teams = 'http://data.nba.net/prod/v2/2022/teams.json'
nba_odds = 'https://api.the-odds-api.com/v4/sports/basketball_nba/odds/?apiKey=d103f4821fd082ddf58190112c6f8832&regions=us&markets=spreads,h2h,totals&oddsFormat=decimal&bookmakers=fanduel'

def json(URL):
    resp = requests.get(URL)
    resp = resp.json()
    return resp
#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------

#Bare starting json
start = json(start_json)
start_links = start['links']

'''
start_links['XXXXX']
___________________
anchorDate
currentDate
calendar
todayScoreboard
currentScoreboard
teams
scoreboard
leagueRosterPlayers
allstarRoster
leagueRosterCoaches
leagueSchedule
leagueConfStandings
leagueDivStandings
leagueUngroupedStandings
leagueMiniStandings
leagueTeamStatsLeaders
leagueLastFiveGameTeamStats
previewArticle
recapArticle
gameBookPdf
boxscore
miniBoxscore
pbp
leadTracker
playerGameLog
playerProfile
playerUberStats
teamSchedule
teamsConfig
teamRoster
teamsConfigYear
teamScheduleYear
teamLeaders
teamScheduleYear2
teamLeaders2
teamICS
teamICS2
playoffsBracket
playoffSeriesLeaders
universalLinkMapping
ticketLink
'''

'/Users/kingmitch/Library/Python/3.7/lib/python/site-packages/nba_api/live/nba'

  
    
    
import nba_api.stats.endpoints as stats_endpoints
import nba_api.live.nba.endpoints as today_endpoints
import pandas



teamIDkey = {'ATL':'1610612737','BRK':'1610612751','BOS':'1610612738','CHA':'1610612766','CLE':'1610612739',
             'CHI':'1610612741', 'DAL':'1610612742', 'DEN':'1610612743', 'DET':'1610612765', 'GSW':'1610612744',
             'HOU':'1610612745', 'IND':'1610612754', 'LAC':'1610612746','LAL':'1610612747','MEM':'1610612763',
             'MIA':'1610612748', 'MIL':'1610612749', 'MIN':'1610612750', 'NYK':'1610612752', 'NOP':'1610612740',
             'OKC':'1610612760', 'ORL':'1610612753', 'PHI':'1610612755', 'PHO':'1610612756','POR':'1610612757',
             'SAS':'1610612759', 'SAC':'1610612758', 'TOR':'1610612761','UTA':'1610612762','WAS':'1610612764'}


def Quarter_Points(gameID):
    BoxScoreSummary = stats_endpoints.boxscoresummaryv2.BoxScoreSummaryV2(gameID)
    BoxScoreSummary = BoxScoreSummary.get_dict()
    BoxScoreSummary = BoxScoreSummary['resultSets']
    BoxScoreSummary = BoxScoreSummary[5]
    headers = BoxScoreSummary['headers']
    data = BoxScoreSummary['rowSet']

    df = pandas.DataFrame(data, columns = headers)
    new = df[['TEAM_ABBREVIATION','PTS_QTR1','PTS_QTR2','PTS_QTR3','PTS_QTR4']]
    print(new)



def get_gameid():
    log = stats_endpoints.teamgamelogs.TeamGameLogs(team_id_nullable = '1610612737', season_nullable = '2022-23')
    log = log.get_dict()
    log = log['resultSets']
    log = log[0]
    headers = log['headers']
    data = log['rowSet']
    df = pandas.DataFrame(data,columns = headers)
    new = df['GAME_ID'].to_list()
    print(type(new))

get_gameid()
    

