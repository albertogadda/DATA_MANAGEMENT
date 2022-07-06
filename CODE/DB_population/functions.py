from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from chessdotcom import get_player_profile,get_leaderboards,get_player_stats,get_player_games_by_month
import berserk
import numpy as np
import pandas as pd
import datetime
from tqdm import tqdm
import re
import sqlite3
import time

def getChessDotComProPlayers(): #Get the list of the best players in 'bullet', 'blitz' and 'rapid' chess categories (meant to be used just once and then be replaced by 'updateChessDotComProPlayers').
    data=get_leaderboards().json['leaderboards']
    bulletLeaderboard = np.array([_['username'] for _ in data['live_bullet']]) #Bullet leaderboard.
    blitzLeaderboard = np.array([_['username'] for _ in data['live_blitz']]) #Blitz leaderboard.
    rapidLeaderboard = np.array([_['username'] for _ in data['live_rapid']]) #Rapid leaderboard.
    # topPlayers = np.unique(np.concatenate([bulletLeaderboard,blitzLeaderboard,rapidLeaderboard])) #List of unique values, containing every player who is in at least one of the leaderboards above.
    return(bulletLeaderboard,blitzLeaderboard,rapidLeaderboard) #Return the output lists.

def getLichessProPlayers(client): #Get the list of the best players in 'bullet', 'blitz' and 'rapid' chess categories (meant to be used just once and then be replaced by 'updateLichessProPlayers').
    bulletLeaderboard = np.array([_['username'] for _ in client.users.get_leaderboard('bullet',50)]) #Bullet leaderboard.
    blitzLeaderboard = np.array([_['username'] for _ in client.users.get_leaderboard('blitz',50)]) #Blitz leaderboard.
    rapidLeaderboard = np.array([_['username'] for _ in client.users.get_leaderboard('rapid',50)]) #Rapid leaderboard.
    # topPlayers = np.unique(np.concatenate([bulletLeaderboard,blitzLeaderboard,rapidLeaderboard])) #List of unique values, containing every player who is in at least one of the leaderboards above.
    return(bulletLeaderboard,blitzLeaderboard,rapidLeaderboard)#Return the output lists.


def scrapeChessDotComOnlineStatus(topPlayers_CDC): #Function to scrape player status from Chess.com.

    op = webdriver.ChromeOptions() #Set Chrome options.
    op.add_argument('headless') #Hide Chrome to enhance speed.
    op.add_argument('--disable-infobars') #Disable infobars. 
    op.add_argument('--disable-extensions') #Disable extensions.

    caps = DesiredCapabilities.CHROME.copy() #Set Chrome capabilities.
    caps['pageLoadStrategy'] = "eager" #Minimise the amount of information requested to the webpage to enhance speed.

    ser = Service('/usr/local/bin/chromedriver') #Load 'chromedriver'.
    driver = webdriver.Chrome(service=ser,options=op,desired_capabilities=caps) #Initiate Chrome session.
    
    resultDataframe = pd.DataFrame(columns=('Time','Player','Online')) #Create the output dataframe.

    for _ in range(len(topPlayers_CDC)): #Excecute loop for every player in the list.
        driver.get('https://www.chess.com/members/' + topPlayers_CDC[_]) #Search for the player on Chess.com.     
        result = driver.find_element(By.XPATH,'//*[@id="view-profile"]/div[1]/div[1]/div/div[2]/div/div[2]/div[3]/div[1]/div[2]').get_attribute('innerHTML') == 'Online Now' #Check if the player is online.
        resultDataframe.loc[_] = [datetime.datetime.now(),topPlayers_CDC[_],result] #Save the results.
    return(resultDataframe) #Return the output dataframe.

def isOnlineOnLichess(topPlayers_LC,client): #Fetch the Lichess status for each player.
    resultDataframe = pd.DataFrame(columns=('Time','Player','Online')) #Create the output dataframe.
    for _ in range(len(topPlayers_LC)):
        try: result = client.users.get_public_data(topPlayers_LC[_])['online'] #Check if the player is online.
        except: result=0
        resultDataframe.loc[_] = [datetime.datetime.now(),topPlayers_LC[_],result] #Save the results.
    return(resultDataframe) #Return the output dataframe.


def get_chessDotCom_profile(player):  #get the available data about the chessDotCom player (player,firstName,lastName,title,country,location)
    data=get_player_profile(player).json['player']

    try: title=data['title']
    except: title=None
    
    try:country=data['country'][-2:]
    except:country=None

    try:location=data['location']
    except:location=None

    try:firstName=data['name'].split(' ')[0]
    except:firstName=None

    try:lastName=data['name'].split(' ')[1]
    except: lastName=None
    
    return({'player':player,'firstname':firstName,'lastname':lastName,'title':title,'country':country,'location':location})


def get_lichess_profile(player, client):  #get the available data about the lichess player (player,firstName,lastName,title,country,location)
    try: public=client.users.get_public_data(player)['profile']
    except: 
        title=None
        country=None
        location=None
        firstName=None
        lastName=None


    try: title=client.users.get_realtime_statuses(player)[0]['title']
    except: title=None

    try: country=public['country']
    except:country=None

    try: location=public['location']   
    except:location=None

    try: firstName=public['firstName']
    except: firstName=None

    try: lastName=public['lastName']
    except: lastName=None

    return({'player':player,'firstname':firstName,'lastname':lastName,'title':title,'country':country,'location':location})



def getChessDotComPlayerRatings(player): #Get player ratings in 'bullet', 'blitz' and 'rapid' chess categories.
    data=get_player_stats(player).json['stats']
    bulletExists = 'chess_bullet' in data.keys() #Check if bullet rating exists.
    blitzExists = 'chess_blitz' in data.keys() #Check if blitz rating exists.
    rapidExists = 'chess_rapid' in data.keys() #Check if rapid rating exists.
    bulletRating = data['chess_bullet']['last']['rating'] if bulletExists else 0 #Get bullet rating if it exists.
    blitzRating = data['chess_blitz']['last']['rating'] if blitzExists else 0 #Get blitz rating if it exists.
    rapidRating = data['chess_rapid']['last']['rating'] if rapidExists else 0 #Get rapid rating if it exists.
    return(bulletRating,blitzRating,rapidRating) #Return the three lists.

def getLichessPlayerRatings(player,client): #Get player ratings in 'bullet', 'blitz' and 'rapid' chess categories.
    try:
        data=client.users.get_public_data(player)['perfs']
        bulletRating = data['bullet']['rating'] #Bullet rating.
        blitzRating = data['blitz']['rating'] #Blitz rating.
        rapidRating = data['rapid']['rating'] #Rapid rating.
    except: 
        bulletRating = 0
        blitzRating = 0
        rapidRating = 0



    return(bulletRating,blitzRating,rapidRating) #Return the three lists.

def query_insert_online(df,platform):
    """questa funzione aggior
    na il db con i valori attuali"""

    test_database='/home/alberto/Desktop/database.db'
    conn = sqlite3.connect(test_database) 
    c = conn.cursor()

    for i in range(0,len(df)):
        my_dict=df.iloc[i]
        columns = ', '.join(my_dict.keys())
        placeholders = ':'+', :'.join(my_dict.keys())
        query = 'INSERT INTO Online_%s (%s) VALUES (%s)' % (platform, columns, placeholders)

        c.execute(query, my_dict)
        conn.commit()


def query_insert_profile(df):
    """questa funzione aggior
    na il db con i valori attuali"""

    test_database='/home/alberto/Desktop/database.db'
    conn = sqlite3.connect(test_database) 
    c = conn.cursor()

    for i in range(0,len(df)):
        my_dict=df.iloc[i]
        columns = ', '.join(my_dict.keys())
        placeholders = ':'+', :'.join(my_dict.keys())
        query = 'INSERT OR REPLACE INTO Player (%s) VALUES (%s)' % (columns, placeholders)

        c.execute(query, my_dict)
        conn.commit()



def query_insert_ranking(df,platform):
    """questa funzione aggior
    na il db con i valori attuali"""

    test_database='/home/alberto/Desktop/database.db'
    conn = sqlite3.connect(test_database) 
    c = conn.cursor()

    for i in range(0,len(df)):
        my_dict=df.iloc[i]
        columns = ', '.join(my_dict.keys())
        placeholders = ':'+', :'.join(my_dict.keys())
        query = 'INSERT INTO Rating_%s (%s) VALUES (%s)' % (platform, columns, placeholders)

        c.execute(query, my_dict)
        conn.commit()
        



def query_insert_match(df, platform):
    """questa funzione aggior
    na il db con i valori attuali"""

    test_database='/home/alberto/Desktop/database.db'
    conn = sqlite3.connect(test_database) 
    c = conn.cursor()

    for i in range(0,len(df)):
        my_dict=df.iloc[i]
        columns = ', '.join(my_dict.keys())
        placeholders = ':'+', :'.join(my_dict.keys())
        query = 'INSERT OR REPLACE INTO Match_%s (%s) VALUES (%s)' % (platform, columns, placeholders)

        c.execute(query, my_dict)
        conn.commit()







def games_chessDotCom(player_list, period):
    df=pd.DataFrame()
    if period==1:
        start_y=2010
        start_m=1
    else:
        start_y=datetime.datetime.now().year
        start_m=datetime.datetime.now().month
    for player in player_list:
        print('BBBB')
        for year in range(start_y,2023):  
            if year!=2022:
                last_month=13
            else:
                last_month=2     
            for month in range(start_m,last_month):
                data=get_player_games_by_month(player, year=year, month=month).games
                for i in tqdm(range(len(data))):
                    rated=data[i].rated
                    try:
                        pgn_def=[]
                        pgn=data[i].pgn
                        pgn=re.sub(" *\{[^\}]*\} *"," ",pgn.split('\n')[len(pgn.split('\n'))-2])[:-4].split(' ')
                        for j in pgn:
                            if '.' not in j:
                                pgn_def.append(j)
                        white=0
                        black=0
                        for _ in data[i].pgn.split('\n'):
                            if 'WhiteElo' in _:
                                white=_[11:15]
                            if 'BlackElo' in _:
                                black=_[11:15]

                    except:
                        pgn_def=0
                        white=0
                        black=0
                    if data[i].black.result=='win':
                        winner='black'  
                    elif data[i].white.result=='win':
                        winner='white'
                    else:
                        winner='tie'
                    diz={'id':data[i].url, 'rules':data[i].rules, 'white':data[i].white.username, 'whiteRate':white, 'black':data[i].black.username, 'blackRate':black, 'winner':winner, 'speed':data[i].time_class, 'time':data[i].end_time , 'pgn':pgn_def }   
                    if diz['rules']=='chess' and rated==True:
                        df=df.append(diz, ignore_index=True)     
    if len(df)>0:
        df.drop(columns=['rules'], inplace=True)
        df['time']=df['time'].apply(lambda x: str(datetime.datetime.fromtimestamp(x)))
    return(df)



def games_lichess(player_list,client, period):
    if period==1:
        start = berserk.utils.to_millis(datetime.datetime(2010,12, 8))
        end = berserk.utils.to_millis(datetime.datetime(2022, 1, 9))
    else:
        start = berserk.utils.to_millis(datetime.datetime.now())
        end = berserk.utils.to_millis(datetime.datetime.now())

    df=pd.DataFrame()
    for player in player_list:
        print('AAA')
        x=list(client.games.export_by_player(player, since=start, until=end, max=10))
        for i in range(1,len(x)):
            if x[i]['variant']=='standard':
                if 'winner' in x[i].keys():
                    winner=x[i]['winner']
                else:
                    winner='tie'
                try: white=x[i]['players']['white']['user']['name']
                except: white='Stockfish'
                
                try: black=x[i]['players']['black']['user']['name']
                except: black='Stockfish'

                try: whiteRate=x[i]['players']['white']['rating']
                except: whiteRate=0

                try: blackRate=x[i]['players']['black']['rating']
                except: blackRate=0

                try: pgn=x[i]['moves'].split(' ')
                except:pgn=0

                try: time=x[i]['lastMoveAt']
                except: time=0

                diz={'id':x[i]['id'], 'white':white, 'whiteRate':whiteRate, 'black':black, 'blackRate':blackRate, 'winner':winner, 'speed':x[i]['speed'], 'time':time, 'pgn':pgn}
                
                df=df.append(diz, ignore_index=True)
    if len(df)>0:
        df['time']=df['time'].apply(lambda x:  str(x)[:-13])

    return(df)


def find_opening(pgn):
    string=pgn
    op = webdriver.ChromeOptions() #Set Chrome options.
    op.add_argument('headless') #Hide Chrome to enhance speed.
    op.add_argument('--disable-infobars') #Disable infobars. 
    op.add_argument('--disable-extensions') #Disable extensions.
    caps = DesiredCapabilities.CHROME.copy() #Set Chrome capabilities.
    caps['pageLoadStrategy'] = "eager" #Minimise the amount of information requested to the webpage to enhance speed.
    ser = Service('/usr/local/bin/chromedriver') #Load 'chromedriver'.
    driver = webdriver.Chrome(service=ser,options=op,desired_capabilities=caps) #Initiate Chrome session.
    driver.get(f'https://www.chess.com/it/explorer?moveList={string}') #Search for the player on Chess.com.   
    time.sleep(0.5)  
    x=driver.page_source
    return x[x.find('eco-classifier-label"><!----> <span>')+len('eco-classifier-label"><!----> <span>')  :  x[x.find('eco-classifier-label"><!----> <span>')+len('eco-classifier-label"><!----> <span>'):].find('</span')+x.find('eco-classifier-label"><!----> <span>')+len('eco-classifier-label"><!----> <span>')]

def clean_pgn_short(i):
    i=i.replace("\'","")
    i=i.replace("[","")
    i=i.replace("'","")
    i=i.replace('"',"")
    i=i.replace(" ","")
    i=i.replace("]","")
    i=i.replace(',','+')
    return i


def add_opening(x):
    x['pgn_short']=x['pgn'].apply(lambda x: str(x.split(",")[0:2]))
    x['pgn_short']=x['pgn_short'].apply(clean_pgn_short)

    k=list(set(x['pgn_short']))

    DF=pd.DataFrame()
    DF['pgn']=k
    DF['opening']=DF['pgn'].apply(find_opening)

    df_with_opening=x.merge(DF, left_on='pgn_short', right_on='pgn', how='left')
    df_with_opening.drop(columns=['pgn_short','pgn_y'], inplace=True)
    df_with_opening.columns=['id', 'white', 'whiteRate', 'black', 'blackRate', 'winner', 'speed','time', 'pgn', 'opening']

    return df_with_opening
    


def clean(x):
    if x!=None:
        badchars=['.','!',':',';','-','_','?','=','$','%','&','/','(',')','^','#','@',' ','0','1','2','3','4','5','6','7','8','9']
        x=x.lower()
        for i in badchars:
            x=x.replace(i,'')
        x=x.replace('à','a')
        x=x.replace('è','e')
        x=x.replace('é','e')
        x=x.replace('ò','o')
        x=x.replace('ù','u')
        x=x.replace('ì','i')
        x=x.replace('ç','c')

    return x

def clean_country(x):
    if x!=None:
        badchars=['.','!',':',';','-','_','?','=','$','%','&','/','(',')','^','#','@',' ','0','1','2','3','4','5','6','7','8','9']
        x=x.lower()
        for i in badchars:
            x=x.replace(i,'')
        x=x.replace('à','a')
        x=x.replace('è','e')
        x=x.replace('é','e')
        x=x.replace('ò','o')
        x=x.replace('ù','u')
        x=x.replace('ì','i')
        x=x.replace('ç','c')
        if len(x)>2:
            x=x[:2]

    return x
