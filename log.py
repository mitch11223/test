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
import pandas
import numpy
import csv
#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------

team_list = ['ATL', 'BOS','BRK', 'CHO', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS','TOR', 'UTA', 'WAS'] 
key = {'ATL':'AtlantaHawks', 'BRK':'BrooklynNets', 'BOS':'BostonCeltics', 'CHO':'CharlotteHornets','CHI':'ChicagoBulls','CLE':'ClevelandCavaliers','DAL':'DallasMavericks','DEN':'DenverNuggets','DET':'DetroitPistons',
           'GSW':'GoldenStateWarriors','HOU':'HoustonRockets','IND':'IndianaPacers','LAC':'LosAngelesClippers','LAL':'LosAngelesLakers','MEM':'MemphisGrizzlies','MIA':'MiamiHeat','MIL':'MilwaukeeBucks','MIN':'MinnesotaTimberwolves',
           'NOP':'NewOrleansPelicans','NYK':'NewYorkKnicks','OKC':'OklahomaCityThunder','ORL':'OrlandoMagic','PHI':'Philadelphia76ers','PHO':'PhoenixSuns','POR':'PortlandTrailBlazers','SAC':'SacramentoKings','SAS':'SanAntonioSpurs','TOR':'TorontoRaptors',
           'UTA':'UtahJazz','WAS':'WashingtonWizards'}
key_2 = {value: key for key, value in key.items()}
t = time.localtime()
current_date = time.strftime("%D",t)
day = int(current_date[3:5])
day = str(day - 1)
day = str('0' + day)
current_date_real = str('20' + current_date[6:8] + '-' + current_date[0:2] + '-' + current_date[3:5]) #real day
current_date = str('20' + current_date[6:8] + '-' + current_date[0:2] + '-' + day) #going back a day because when this is run it is the next day
script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)
print(current_date)
#FILE MANAGMENT____

filenamealt = str('TeamFiles/League/Stakes/Days/2023/' + current_date)
#filenamealt = str('TeamFiles/League/Stakes/' + '2022-11-25')
os.makedirs(os.path.dirname(filenamealt + '/daily_return_per_oddrange.txt'), exist_ok=True)
os.makedirs(os.path.dirname('TeamFiles/League/Stakes/stake_log.txt'), exist_ok=True)

#daily_return_per_oddrange records proft/loss for each odds range per day
daily_return_per_oddrange = open(filenamealt + '/daily_return_per_oddrange.txt', 'a+')
#daily_return_per_oddrange.truncate(0) #resets daily returns by oddrange

#stake_record_alltime records the alltime wins/losses per stake amount (odds recorded too)
stake_record_alltime = open('TeamFiles/League/Stakes/stake_log.txt', 'a+')


#open league schedule to pull and automatically append the team opponent to betlog list
league_schedule = pandas.read_csv('TeamFiles/League/Schedule/Full_Schedule.txt')
today_schedule = league_schedule[['Date','Visitor/Neutral','Home/Neutral']]
today_schedule = today_schedule.loc[today_schedule['Date'] == current_date]
#today_schedule = today_schedule.loc[today_schedule['Date'] == '2022-11-25']

#Write headers for csv outputs
daily_return_per_oddrange.write('\n' + 'Odds_Range,Profit/Loss' + '\n')
#make sure not to write headers everytime the all time stake record file is updated
if os.stat('TeamFiles/League/Stakes/stake_log.txt').st_size == 0:
    stake_record_alltime.write('Date,Stake,Odds,Result,Opponent,Team,Return,Type' + '\n')
else:
    pass
    
    
    
    
betlog = []
stake_extra = [] #less than 2
stake1 = [] #2.00 - 2.49
stake2 = [] #2.50 - 2.99
stake3 = [] #3.00 - 3.49
stake4 = [] #3.50 - 3.99
stake5 = [] #4.00 - 5.99
stake6 = [] #6.00 +
sumreslist = []
stake_key = {'stake1':'2.00-2.49','stake2':'2.50-2.99','stake3':'3.00-3.49','stake4':'3.50-3.99','stake5':'4.00-5.99','stake6':'6.00+','stake_extra':'1.00-1.99'}


#input all bets at same time
def grab_info():
    while True:
        team = input('What Team')
        if team != '':
            odds = float(input('What Odds'))
            stake = float(input('What Stake'))
            result = input('Result')
            Type = input('What Type:')
            try:
                if key[team] in today_schedule['Visitor/Neutral'].unique():
                    opponent = today_schedule.loc[today_schedule['Visitor/Neutral'] == key[team], 'Home/Neutral']
                    for Team in opponent:
                        opponent = key_2[Team]
                    print(opponent)
                    if result == 'L':
                        pl = -1*(stake)
                    elif result == 'W':
                        pl = (stake*odds)-stake
                    betlog.append([team,odds,stake,result,opponent,pl,Type])
                                                                  
                elif key[team] in today_schedule['Home/Neutral'].unique():
                    opponent = today_schedule.loc[today_schedule['Home/Neutral'] == key[team], 'Visitor/Neutral']
                    for Team in opponent:
                        opponent = key_2[Team]
                    print(opponent)
                    if result == 'L':
                        pl = -stake
                    elif result == 'W':
                        pl = ((stake*odds)-stake)
                    betlog.append([team,odds,stake,result,opponent,pl,Type])
                else:
                    print('Team did not play today...')
            except KeyError:
                print('Team Not Valid')
                pass
        else:
            break
    


#this function grabs the inputted data and organizes it into lists
def log_process():
    for bet in betlog:
        team = bet[0]
        odds = bet[1]
        stake = bet[2]
        result = bet[3]
        opponent = bet[4]
        pl = bet[5]
        Type = bet[6]
        filename = str('TeamFiles/' + key[team] + '/Stakes/' +  current_date + '/' + 'teamstakes.txt')
        #filename = str('TeamFiles/' + key[team] + '/Stakes/' +  '2022-11-25' + '/' + 'teamstakes.txt')
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        file = open(filename, 'a+')
        
        if os.stat(filename).st_size == 0:
            file.write('Current_Date,Stake,Odds,Result,Opponent,Return,Type' + '\n')
        else:
            pass
        
        
        #write odds,stake,profit/loss,win or lose per team
        file.write(current_date + ',' + str(stake) + ',' + str(odds) + ',' + result + ',' + opponent + ',' + str(pl) + ',' + Type + '\n')
        file.close()
        #need to log bets by odds range
        #need to log bets by team
        if 2 < odds < 2.49:
            stake1.append(bet)
        elif 2.5 < odds < 2.99:
            stake2.append(bet)
        elif 3 < odds < 3.49:
            stake3.append(bet)
        elif 3.5 < odds < 3.99:
            stake4.append(bet)
        elif 4 < odds < 5.99:
            stake5.append(bet)
        elif 6 < odds:
            stake6.append(bet)
        else:
            stake_extra.append(bet)


def calculate():
    #multiply either 0 or stake by odds for each list
    #find out how many 4 dollar bets win vs lose depednednt and independant of odds
    fullstakes = [stake1,stake2,stake3,stake4,stake5,stake6,stake_extra]
    stakewins = []
    stakelosses = []
    #for each odds range
    for partition in fullstakes:
        sum_result = []
        #for each bet in odd range
        for bet in partition:
            result = float(0)
            team = bet[0]
            stake = bet[2]
            odds = bet[1]
            opponent = bet[4]
            pl = bet[5]
            Type = bet[6]
            if 'W' in bet:
                result = (bet[1]*stake) - stake
                stakewins.append([stake,odds])
                stake_record_alltime.write(current_date + ',' + str(stake) + ',' + str(odds) + ',W,' + opponent + ',' + team + ',' + str(pl) + ',' + Type + '\n')
                
            elif 'L' in bet:
                result = -1*(stake)
                stakelosses.append([stake,odds])
                stake_record_alltime.write(current_date + ',' + str(stake) + ',' + str(odds) + ',L,' + opponent + ',' + team + ',' + str(pl) + ',' + Type + '\n')
            else:
                print('No Win Or Loss?')
                pass
                
            sum_result.append(result)
        sumres = sum(sum_result)
        sumreslist.append(sumres)
    print(sumreslist)
    stake_record_alltime.close()    
    #this assigns profit/loss values of each odd criteria
    extra = stake_key['stake_extra']
    extra_result = sumreslist[6]
    one = stake_key['stake1']
    one_result = sumreslist[0]
    two = stake_key['stake2']
    two_result = sumreslist[1]
    three = stake_key['stake3']
    three_result = sumreslist[2]
    four = stake_key['stake4']
    four_result = sumreslist[3]
    five = stake_key['stake5']
    five_result = sumreslist[4]
    six = stake_key['stake6']
    six_result = sumreslist[5]
    total_result = (float(extra_result) + float(one_result) + float(two_result) + float(three_result) + float(four_result) + float(five_result + float(six_result)))
  
    
    #writes profit or loss per odd range(ie 2-2.5,2.5-3 etc...)
    daily_return_per_oddrange.write(extra + ',' + str(extra_result) + '\n' + one + ',' + str(one_result) + '\n' + two + ',' + str(two_result) + '\n' + three + ',' + str(three_result) + '\n' + four + ',' + str(four_result) + '\n' + five + ',' + str(five_result) + '\n' + six + ',' + str(six_result) + '\n' +'Total' + ',' + str(total_result))
    daily_return_per_oddrange.close()
    
    
    
    print(extra,': ', extra_result)
    print(one,': ',one_result)
    print(two,': ',two_result)
    print(three,': ',three_result)
    print(four,': ',four_result)
    print(five,': ',five_result)
    print(six,': ',six_result)
    print('Total: ',total_result)
    print('-----------')       






def execute(): 
    grab_info()
    print('Logged')
    log_process()
    print('Written to lists and files')
    print('\n')
    calculate()
    print('Calculating Done')
    print('\n')
    print('Importing logtester.py...')
    import logtester
    print('Initiating all_time Class')
    all_time = logtester.all_time()
    print('Executing league_odd_partition_alltime() method')
    all_time.league_odd_partition_alltime()
    print('Executing team_odd_partition_alltime() method')
    all_time.team_odd_partition_alltime('Team')
    print('Executing opponent partition...')
    all_time.team_odd_partition_alltime('Opponent')
    print('Done!')
    
    

    
#ONLY EXECUTE THIS WHEN SURE --- HARD TO REDO STUFF IF MESS UP   
execute()    


