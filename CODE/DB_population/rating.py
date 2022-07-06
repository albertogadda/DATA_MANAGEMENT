from codecs import ignore_errors
from functions import getLichessPlayerRatings, getChessDotComPlayerRatings, query_insert_ranking, getLichessProPlayers, getChessDotComProPlayers
import berserk
import pandas as pd
import datetime
import sqlite3
import time

def rating(time):
    test_database='/home/alberto/Desktop/database.db'
    conn = sqlite3.connect(test_database) 
    c = conn.cursor()  

    c.execute('''
            CREATE TABLE IF NOT EXISTS Rating_lichess
            ([id] INTEGER PRIMARY KEY AUTOINCREMENT, [time] TEXT, [player] TEXT,  [rating] INTEGER, [speed] TEXT)
            ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS Rating_chessDotCom
        ([id] INTEGER PRIMARY KEY AUTOINCREMENT, [time] TEXT, [player] TEXT,  [rating] INTEGER, [speed] TEXT)
        ''')
            
                            
    conn.commit()

    client = berserk.Client(session=berserk.TokenSession('lip_tASmazZwz0V835hoPxGH')) #Authentication in the Lichess API.

    li_bu,li_bl,li_ra=getLichessProPlayers(client)
    li_bu_df=pd.DataFrame()
    li_bu_df['player']=li_bu
    li_bu_df['speed']='bullet'
    li_bl_df=pd.DataFrame()
    li_bl_df['player']=li_bl
    li_bl_df['speed']='blitz'
    li_ra_df=pd.DataFrame()
    li_ra_df['player']=li_ra
    li_ra_df['speed']='rapid'
    old_li=li_bu_df.append(li_bl_df.append(li_ra_df, ignore_index=True),ignore_index=True)

    ch_bu,ch_bl,ch_ra=getChessDotComProPlayers()
    ch_bu_df=pd.DataFrame()
    ch_bu_df['player']=ch_bu
    ch_bu_df['speed']='bullet'
    ch_bl_df=pd.DataFrame()
    ch_bl_df['player']=ch_bl
    ch_bl_df['speed']='blitz'
    ch_ra_df=pd.DataFrame()
    ch_ra_df['player']=ch_ra
    ch_ra_df['speed']='rapid'
    old_ch=ch_bu_df.append(ch_bl_df.append(ch_ra_df, ignore_index=True),ignore_index=True)


    lichess=pd.DataFrame()
    for i in range(len(old_li)):
        if old_li.iloc[i]['speed']=='bullet':      
            lichess=lichess.append({'player':old_li.iloc[i]['player'], 'speed':'bullet', 'rating': getLichessPlayerRatings(old_li.iloc[i]['player'], client)[0]}, ignore_index=True)
        if old_li.iloc[i]['speed']=='blitz':      
            lichess=lichess.append({'player':old_li.iloc[i]['player'], 'speed':'blitz', 'rating': getLichessPlayerRatings(old_li.iloc[i]['player'], client)[1]}, ignore_index=True)
        elif old_li.iloc[i]['speed']=='rapid':      
            lichess=lichess.append({'player':old_li.iloc[i]['player'], 'speed':'rapid', 'rating': getLichessPlayerRatings(old_li.iloc[i]['player'], client)[2]}, ignore_index=True)
    
    chess=pd.DataFrame()
    for i in range(len(old_ch)):
        if old_ch.iloc[i]['speed']=='bullet':      
            chess=chess.append({'player':old_ch.iloc[i]['player'], 'speed':'bullet', 'rating': getChessDotComPlayerRatings(old_ch.iloc[i]['player'])[0]}, ignore_index=True)
        if old_ch.iloc[i]['speed']=='blitz':      
            chess=chess.append({'player':old_ch.iloc[i]['player'], 'speed':'blitz', 'rating': getChessDotComPlayerRatings(old_ch.iloc[i]['player'])[1]}, ignore_index=True)
        elif old_ch.iloc[i]['speed']=='rapid':      
            chess=chess.append({'player':old_ch.iloc[i]['player'], 'speed':'rapid', 'rating': getChessDotComPlayerRatings(old_ch.iloc[i]['player'])[2]}, ignore_index=True)
    


    
    lichess['time']=time
    chess['time']=time

    query_insert_ranking(lichess,'lichess')
    query_insert_ranking(chess,'chessDotCom')




if __name__ == "__main__":
    while True:
    
        rating('kkk')
        time.sleep(5)