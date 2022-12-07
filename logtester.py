import time
import os
import pandas
import requests
from bs4 import BeautifulSoup
import re

script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)


#------------------


team_list = ['ATL', 'BRK','BOS', 'CHO', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS','TOR', 'UTA', 'WAS'] 
key = {'ATL':'AtlantaHawks', 'BRK':'BrooklynNets', 'BOS':'BostonCeltics', 'CHO':'CharlotteHornets','CHI':'ChicagoBulls','CLE':'ClevelandCavaliers','DAL':'DallasMavericks','DEN':'DenverNuggets','DET':'DetroitPistons',
           'GSW':'GoldenStateWarriors','HOU':'HoustonRockets','IND':'IndianaPacers','LAC':'LosAngelesClippers','LAL':'LosAngelesLakers','MEM':'MemphisGrizzlies','MIA':'MiamiHeat','MIL':'MilwaukeeBucks','MIN':'MinnesotaTimberwolves',
           'NOP':'NewOrleansPelicans','NYK':'NewYorkKnicks','OKC':'OklahomaCityThunder','ORL':'OrlandoMagic','PHI':'Philadelphia76ers','PHO':'PhoenixSuns','POR':'PortlandTrailBlazers','SAC':'SacramentoKings','SAS':'SanAntonioSpurs','TOR':'TorontoRaptors',
           'UTA':'UtahJazz','WAS':'WashingtonWizards'}
#------------------


    
class all_time:
    #one function for wl by odds range everything
    #one function for wl by odds range per team
    #one function for wl by odds range opponent
    def __init__(self):
        #self.teamstakedir = str('TeamFiles/' + key[team] +'/Stakes/')
        self.leaguestakedir = 'TeamFiles/League/Stakes/Days/2023/'
        self.leaguestakelogdir = 'TeamFiles/League/Stakes/stake_log.txt'

    def league_odd_partition_alltime(self):
        #wl by odds range for everything
        filedir = 'TeamFiles/League/Stakes/odd_partition_alltime.txt'
        stake_key = ['1.00-1.99','2.00-2.49','2.50-2.99','3.00-3.49','3.50-3.99','4.00-5.99','6.00+','Total']
        os.makedirs(os.path.dirname(filedir),exist_ok=True)
        alltimefile = open(filedir,'a+')
        alltimefile.truncate(0)

        numbers = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]

        alltimetotallists = []

        #grabs the odd partition numbers for each day in Stakes/days file
        for subdir, dirs, files in os.walk(self.leaguestakedir):
            for day in dirs:
                parse = pandas.read_csv(self.leaguestakedir + day + '/daily_return_per_oddrange.txt')
                pl = []
                for element in parse['Profit/Loss']:
                    pl.append(element)
                    element = float(element)
                alltimetotallists.append(pl)


        alltimetotal = [sum(x) for x in zip(*alltimetotallists)]


        #writes the alltime totals per odd partition
        for i in range(len(alltimetotal)):
            total = (str(stake_key[i]) + ',' + str(alltimetotal[i]) + '\n')
            alltimefile.write(total)
        alltimefile.close()
        
    def team_odd_partition_alltime(self,OpponentOrTeam):
        self.option = OpponentOrTeam
        filedir = str('TeamFiles/League/Stakes/TeamOpponentReturns/' + self.option + '/_partition_log.txt')
        wlfiledir = str('TeamFiles/League/Stakes/TeamOpponentWinLossPartitions/' + self.option + '/_winlosspartition_log.txt')
        os.makedirs(os.path.dirname(filedir),exist_ok=True)
        os.makedirs(os.path.dirname(wlfiledir),exist_ok=True)
        team_log_file = open(filedir,'a+')
        team_log_file.truncate(0)
        wl_log_file = open(wlfiledir,'a+')
        wl_log_file.truncate(0)
        stake_key = {'stake1':'2.00-2.49','stake2':'2.50-2.99','stake3':'3.00-3.49','stake4':'3.50-3.99','stake5':'4.00-5.99','stake6':'6.00+','stake_extra':'1.00-1.99'}
        for team in team_list:
            stake_extra = [] #less than 2
            stake1 = [] #2.00 - 2.49
            stake2 = [] #2.50 - 2.99
            stake3 = [] #3.00 - 3.49
            stake4 = [] #3.50 - 3.99
            stake5 = [] #4.00 - 5.99
            stake6 = [] #6.00 +
            sumretlist = []
            wl_list = []
            flname = str('TeamFiles/' + key[team] + '/Stakes/')
            for subdir, dirs, files in os.walk(flname):
                for day in dirs:
                    parse = pandas.read_csv(flname + day + '/teamstakes.txt')                    
                    odds = parse['Odds']
                    odds = odds.tolist()
                    for element in odds:
                        if 2 < element < 2.49:
                            s = parse.loc[parse['Odds'] == element, 'Stake'].tolist()
                            if len(s) > 1:
                                s = s[0]
                            try:
                                for e in s:
                                    s = float(e)
                            except TypeError:
                                pass
                            try:
                                p = parse.loc[parse['Odds'] == element, 'Return'].tolist()
                                if len(p) > 1:
                                    p = p[0]
                                try:
                                    for j in p:
                                        p = float(j)
                                except TypeError:
                                    pass
                                if 0 < p:
                                    r = 'W'
                                elif 0 > p:
                                    r = 'L'
                                else:
                                    print('Return neither higher or lower than 0?')
                                try:
                                    stake1.append([element,s,p,r])
                                except NameError:
                                    pass
                            except KeyError:
                                pass
                            
                        elif 2.5 < element < 2.99:
                            s = parse.loc[parse['Odds'] == element, 'Stake'].tolist()
                            if len(s) > 1:
                                s = s[0]
                            try:
                                for e in s:
                                    s = float(e)
                            except TypeError:
                                pass
                            try:
                                p = parse.loc[parse['Odds'] == element, 'Return'].tolist()
                                if len(p) > 1:
                                    p = p[0]
                                try:
                                    for j in p:
                                        p = float(j)
                                except TypeError:
                                    pass
                                if 0 < p:
                                    r = 'W'
                                elif 0 > p:
                                    r = 'L'
                                else:
                                    print('Return neither higher or lower than 0?')
                                try:
                                    stake2.append([element,s,p,r])
                                except NameError:
                                    pass
                            except KeyError:
                                pass
                            
                    
                        elif 3 < element < 3.49:
                            s = parse.loc[parse['Odds'] == element, 'Stake'].tolist()
                            if len(s) > 1:
                                s = s[0]
                            try:
                                for e in s:
                                    s = float(e)
                            except TypeError:
                                pass
                            try:
                                p = parse.loc[parse['Odds'] == element, 'Return'].tolist()
                                if len(p) > 1:
                                    p = p[0]
                                try:
                                    for j in p:
                                        p = float(j)
                                except TypeError:
                                    pass
                                if 0 < p:
                                    r = 'W'
                                elif 0 > p:
                                    r = 'L'
                                else:
                                    print('Return neither higher or lower than 0?')
                                try:
                                    stake3.append([element,s,p,r])
                                except NameError:
                                    pass
                            except KeyError:
                                pass
                            
                        elif 3.5 < element < 3.99:
                            s = parse.loc[parse['Odds'] == element, 'Stake'].tolist()
                            if len(s) > 1:
                                s = s[0]
                            try:
                                for e in s:
                                    s = float(e)
                            except TypeError:
                                pass
                            try:
                                p = parse.loc[parse['Odds'] == element, 'Return'].tolist()
                                if len(p) > 1:
                                    p = p[0]
                                try:
                                    for j in p:
                                        p = float(j)
                                except TypeError:
                                    pass
                                if 0 < p:
                                    r = 'W'
                                elif 0 > p:
                                    r = 'L'
                                else:
                                    print('Return neither higher or lower than 0?')
                                try:
                                    stake4.append([element,s,p,r])
                                except NameError:
                                    pass
                            except KeyError:
                                pass
                            
                        elif 4 < element < 5.99:
                            s = parse.loc[parse['Odds'] == element, 'Stake'].tolist()
                            if len(s) > 1:
                                s = s[0]
                            try:
                                for e in s:
                                    s = float(e)
                            except TypeError:
                                pass
                            try:
                                p = parse.loc[parse['Odds'] == element, 'Return'].tolist()
                                if len(p) > 1:
                                    p = p[0]
                                try:
                                    for j in p:
                                        p = float(j)
                                except TypeError:
                                    pass
                                if 0 < p:
                                    r = 'W'
                                elif 0 > p:
                                    r = 'L'
                                else:
                                    print('Return neither higher or lower than 0?')
                                try:
                                    stake5.append([element,s,p,r])
                                except NameError:
                                    pass
                            except KeyError:
                                pass
                            
                        elif 6 < element:
                            s = parse.loc[parse['Odds'] == element, 'Stake'].tolist()
                            if len(s) > 1:
                                s = s[0]
                            try:
                                for e in s:
                                    s = float(e)
                            except TypeError:
                                pass
                            try:
                                p = parse.loc[parse['Odds'] == element, 'Return'].tolist()
                                if len(p) > 1:
                                    p = p[0]
                                try:
                                    for j in p:
                                        p = float(j)
                                except TypeError:
                                    pass
                                if 0 < p:
                                    r = 'W'
                                elif 0 > p:
                                    r = 'L'
                                else:
                                    print('Return neither higher or lower than 0?')
                                try:
                                    stake6.append([element,s,p,r])
                                except NameError:
                                    pass
                            except KeyError:
                                pass
                            
                        else:
                            s = parse.loc[parse['Odds'] == element, 'Stake'].tolist()
                            if len(s) > 1:
                                s = s[0]
                            try:
                                for e in s:
                                    s = float(e)
                            except TypeError:
                                pass
                            try:
                                p = parse.loc[parse['Odds'] == element, 'Return'].tolist()
                                if len(p) > 1:
                                    p = p[0]
                                try:
                                    for j in p:
                                        p = float(j)
                                except TypeError:
                                    pass
                                if 0 < p:
                                    r = 'W'
                                elif 0 > p:
                                    r = 'L'
                                else:
                                    print('Return neither higher or lower than 0?')
                            except KeyError:
                                pass
                            try:
                                stake_extra.append([element,s,p,r])
                            except NameError:
                                pass
                  
                
            #print(team,stake1,stake2,stake3,stake4,stake5,stake6,stake_extra)
            stake_list = [stake_extra,stake1,stake2,stake3,stake4,stake5,stake6]
            #print(team,stake4)
            for partition in stake_list:
                sum_return = []
                sum_wins = 0
                sum_losses = 0
                for bet in partition:
                    Odds = bet[0]
                    Stake = bet[1]
                    Return = bet[2]
                    Result = bet[3]
                    
                    if Result == 'W':
                        sum_wins += 1
                    elif Result == 'L':
                        sum_losses += 1
                        
                    
                    sum_return.append(Return)
                #print(team,partition)
                sum_ret = sum(sum_return)
                wl_list.append([sum_wins,sum_losses])
                
                sumretlist.append(sum_ret)
            #this assigns profit/loss values of each odd criteria
            extra = stake_key['stake_extra']
            extra_result = sumretlist[0]
            extra_w = wl_list[0][0]
            extra_l = wl_list[0][1]
            
            one = stake_key['stake1']
            one_result = sumretlist[1]
            one_w = wl_list[1][0]
            one_l = wl_list[1][1]
            
            two = stake_key['stake2']
            two_result = sumretlist[2]
            two_w = wl_list[2][0]
            two_l = wl_list[2][1]
            
            three = stake_key['stake3']
            three_result = sumretlist[3]
            three_w = wl_list[3][0]
            three_l = wl_list[3][1]
            
            four = stake_key['stake4']
            four_result = sumretlist[4]
            four_w = wl_list[4][0]
            four_l = wl_list[4][1]
            
            five = stake_key['stake5']
            five_result = sumretlist[5]
            five_w = wl_list[5][0]
            five_l = wl_list[5][1]
            
            six = stake_key['stake6']
            six_result = sumretlist[6]
            six_w = wl_list[6][0]
            six_l = wl_list[6][1]
            
       
            total_result = (float(extra_result) + float(one_result) + float(two_result) + float(three_result) + float(four_result) + float(five_result + float(six_result)))
            
            
                
                
    
            #writes profit or loss per odd range(ie 2-2.5,2.5-3 etc...)
            team_log_file.write('\n' + '\n' + team + ':' + '\n' + '\n' + extra + ',' + str(extra_result) + '\n' + one + ',' + str(one_result) + '\n' + two + ',' + str(two_result) + '\n' + three + ',' + str(three_result) + '\n' + four + ',' + str(four_result) + '\n' + five + ',' + str(five_result) + '\n' + six + ',' + str(six_result) + '\n' +'Total' + ',' + str(total_result) + '\n')
            wl_log_file.write('\n' + '\n' + team + ':' + '\n' + '\n' + extra + ',' + str(extra_w) + ',' + str(extra_l) + '\n' + one + ',' + str(one_w) + ',' + str(one_l) + '\n' + two + ',' + str(two_w) + ',' + str(two_l) + '\n' + three + ',' + str(three_w) + ',' + str(three_l) + '\n' + four + ',' + str(four_w) + ',' + str(four_l) + '\n' + five + ',' + str(five_w) + ',' + str(five_l) + '\n' + six + ',' + str(six_w) + ',' + str(six_l) + '\n')
            #instead of writing sum of each partition, write count of W or L per parititon
            
            
            
            
            
        wl_log_file.close()      
        team_log_file.close()
        print('team_log_file_updated!')
        
        
    def cleaning_the_glass(self):
        
        
        def spread_calculations(row):
            margin = (int(row['TeamPts'] - int(row['OpponentPts'])))
            if row['Spread'] < 0 and margin > 0:        
                spread_margin = (float(row['Spread']) + margin)
            elif row['Spread'] < 0 and margin < 0:
                spread_margin = (float(row['Spread']) + margin)
            elif row['Spread'] > 0 and margin > 0:
                spread_margin = (float(row['Spread']) + margin)
            elif row['Spread'] > 0 and margin < 0:
                spread_margin = (float(row['Spread']) + margin)
            elif row['Spread'] == 0:
                spread_margin = margin
            else:
                print('somethings wrong...')
            return spread_margin

        def game_margin(row):
            margin = (int(row['TeamPts'] - int(row['OpponentPts'])))
            return margin
        
        #one iteration per team
        lfstr = str('TeamFiles/League/Schedule/SpreadDay.txt')
        os.makedirs(os.path.dirname(lfstr),exist_ok=True)
        lf = open(lfstr,'w+')
        lf.truncate(0)
        lf.write('Spread,Date,Spread_Margin,Opponent,Team' + '\n')
        for i in range(1,30):
            #time.sleep(5)
            print(team_list[i-1])
            print(i)
            link = str('https://cleaningtheglass.com/stats/team/' + str(i) + '/gamelogs')  #tab-four_factors'
            filename = str('TeamFiles/' + key[team_list[i-1]] + '/CTGFourFactors/game_log.txt')
            os.makedirs(os.path.dirname(filename),exist_ok=True)
            teamdf = pandas.read_html(link)
            f = open(filename,'w+')
            f.truncate(0)
            teamdf = teamdf[0]
            teamdf.dropna(how='all',axis=1,inplace=True)
            teamdf.columns = ['Date','Home/Away','Opponent','W/L','TeamPts','OpponentPts','Spread','Off-Pts/Poss%','Off-Pts/Poss#','Off-eFG%','Off-eFG#','Off-TOV%','Off-TOV#','Off-ORB%','Off-ORB#','Off-FT-Rate%','Off-FT-Rate#','Def-Pts/Poss%','Def-Pts/Poss#','Def-eFG%','Def-eFG#','Def-TOV%','Def-TOV#','Def-ORB%','Def-ORB#','Def-FT-Rate%','Def-FT-Rate#']


            teamdf['GameMargin'] = teamdf.apply (lambda row: game_margin(row), axis=1)
            teamdf['SpreadMargin'] = teamdf.apply (lambda row: spread_calculations(row), axis=1)
            teamdf = teamdf.iloc[::-1]
            teamdf['Opponent'] = teamdf['Opponent'].replace('PHX','PHO')
            teamdf['Opponent'] = teamdf['Opponent'].replace('BKN','BRK')
            
            #teamdf.apply (lambda row: spread_calculations(row), axis=1)                                          
            T = team_list[i-1]
            S = teamdf['Spread'].to_list()
            D = teamdf['Date'].to_list()
            SM = teamdf['SpreadMargin'].to_list()
            O = teamdf['Opponent'].to_list()
            
            
            print(teamdf)
            print(len(O))
            print(len(S))
                  
            
            nD = []
            for day in D:
                year = str(day[6:8])
                year = '20' + year
                Day = str(day[3:5])
                month = str(day[0:2])
                NewDay = str(year + '-' + month + '-' + Day)
                nD.append(NewDay)
                
            for e in range(len(S)):
                lf.write(str(S[e]) + ',' + nD[e] + ',' + str(SM[e]) + ',' + O[e] + ',' + T + '\n') 
            
            
            csv = teamdf.to_csv(index = False)
            f.write(csv)
            f.close()
        lf.close()

