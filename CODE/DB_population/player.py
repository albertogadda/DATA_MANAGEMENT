from functions import clean_country, getChessDotComProPlayers, getLichessProPlayers, get_lichess_profile, get_chessDotCom_profile, query_insert_profile, clean, clean_country
import berserk
import pandas as pd
import numpy as np
import sqlite3
import time

def player():
    test_database='/home/alberto/Desktop/database.db'
    conn = sqlite3.connect(test_database) 
    c = conn.cursor()  

    c.execute('''
            CREATE TABLE IF NOT EXISTS Player
            ([ID] INTEGER PRIMARY KEY AUTOINCREMENT, [firstname] TEXT,[lastname] TEXT, [title] TEXT, [country] TEXT, [location] TEXT, [username_lichess] TEXT, [username_chessDotCom] TEXT)
            ''')       
                            
    conn.commit()

    client = berserk.Client(session=berserk.TokenSession('lip_tASmazZwz0V835hoPxGH')) #Authentication in the Lichess API.


    query = 'SELECT * FROM Player'

    old_table=c.execute(query).fetchall()
    old_table=pd.DataFrame(old_table)
    if len(old_table)>0:
        old_table.columns=['id','firstname','lastname','title','country','location','username_lichess','username_chessDotCom']
        old_table.drop(columns=['id'],inplace=True)
    else:
        old_table=pd.DataFrame(columns=['firstname','lastname','title','country','location','username_lichess','username_chessDotCom'])



    lichess= np.unique(np.concatenate([getLichessProPlayers(client)]))
    chess=np.unique(np.concatenate([getChessDotComProPlayers()]))


    lichess_profile=pd.DataFrame()
    for i in lichess:
        if i not in list(old_table['username_lichess']):
            k=get_lichess_profile(i,client)
            lichess_profile=lichess_profile.append(k, ignore_index=True)

    chess_profile=pd.DataFrame()
    for i in chess:
        if i not in list(old_table['username_chessDotCom']):
            k=get_chessDotCom_profile(i)
            chess_profile=chess_profile.append(k, ignore_index=True)

    if(len(lichess_profile))>0:
        lichess_profile['firstname']=lichess_profile['firstname'].apply(clean)
        lichess_profile['lastname']=lichess_profile['lastname'].apply(clean)
        lichess_profile['country']=lichess_profile['country'].apply(clean_country)
    if len(chess_profile)>0:
        chess_profile['firstname']=chess_profile['firstname'].apply(clean)
        chess_profile['lastname']=chess_profile['lastname'].apply(clean)
        chess_profile['country']=chess_profile['country'].apply(clean_country)


    for j in range(len(lichess_profile)):
        k=0
        for i in range(len(old_table)):
            if (old_table.loc[i]['firstname']==lichess_profile.loc[j]['firstname']) and ((old_table.loc[i]['lastname']==lichess_profile.loc[j]['lastname'])) and (old_table.loc[i]['lastname'] != None) and (old_table.loc[i]['lastname']!=None):
                old_table.loc[i]['username_lichess']=lichess_profile.loc[j]['player']
                k=1
        if k==0:
            old_table=old_table.append({'firstname':lichess_profile.loc[j]['firstname'],'lastname':lichess_profile.loc[j]['lastname'],'title':lichess_profile.loc[j]['title'],'country':lichess_profile.loc[j]['country'],'location':lichess_profile.loc[j]['location'],'username_lichess':lichess_profile.loc[j]['player'],'username_chessDotCom':None}, ignore_index=True)


    for j in range(len(chess_profile)):
        k=0
        for i in range(len(old_table)):
            if (old_table.loc[i]['firstname']==chess_profile.loc[j]['firstname']) and ((old_table.loc[i]['lastname']==chess_profile.loc[j]['lastname'])) and (old_table.loc[i]['lastname'] != None) and (old_table.loc[i]['lastname']!=None):
                old_table.loc[i]['username_chessDotCom']=chess_profile.loc[j]['player']
                k=1
        if k==0:
            old_table=old_table.append({'firstname':chess_profile.loc[j]['firstname'],'lastname':chess_profile.loc[j]['lastname'],'title':chess_profile.loc[j]['title'],'country':chess_profile.loc[j]['country'],'location':chess_profile.loc[j]['location'],'username_lichess':None,'username_chessDotCom':chess_profile.loc[j]['player']}, ignore_index=True)






    #va a cercare per username i giocatori sull'altra piattaforma
    #controlla che siano uguali nome,cognome,title e country

    for i in range(len(old_table['username_lichess'])):
        if old_table.loc[i]['username_lichess']==None:
            try:
                pp=get_lichess_profile(old_table.loc[i]['username_chessDotCom'],client)
                if (old_table.loc[i]['firstname']==pp['firstname']) and (old_table.loc[i]['lastname']==pp['lastname']) and (old_table.loc[i]['title']==pp['title']) and (old_table.loc[i]['country']==pp['country']):
                    old_table.loc[i]['username_lichess']=pp['player']
            except:
                o=0

    for i in range(len(old_table['username_chessDotCom'])):
        if old_table.loc[i]['username_chessDotCom']==None:
            try:
                pp=get_chessDotCom_profile(old_table.loc[i]['username_lichess'],client)
                if (old_table.loc[i]['firstname']==pp['firstname']) and (old_table.loc[i]['lastname']==pp['lastname']) and (old_table.loc[i]['title']==pp['title']) and (old_table.loc[i]['country']==pp['country']):
                    old_table.loc[i]['username_chessDotCom']=pp['player']
            except:
                o=0








    query='UPDATE sqlite_sequence SET seq=0 WHERE name = "Player";'
    c.execute(query)
    conn.commit()

    query='DELETE FROM Player'
    c.execute(query)
    conn.commit()

    query_insert_profile(old_table)


if __name__ == "__main__":
    while True:
        player()
        time.sleep(10)