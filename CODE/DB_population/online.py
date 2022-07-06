from functions import scrapeChessDotComOnlineStatus, isOnlineOnLichess, query_insert_online
import berserk
import sqlite3
import datetime
import time


def online(time):
    test_database='/home/alberto/Desktop/database.db'
    conn = sqlite3.connect(test_database) 
    c = conn.cursor()  
    client = berserk.Client(session=berserk.TokenSession('lip_tASmazZwz0V835hoPxGH')) #Authentication in the Lichess API.

    query_li = "SELECT DISTINCT username_lichess FROM Player"
    query_ch = "SELECT DISTINCT username_chessDotCom FROM Player"
      
    lichess_player=c.execute(query_li).fetchall()
    lichess_player=[lichess_player[_][0] for _ in range(len(lichess_player))]

    chess_player=c.execute(query_ch).fetchall()
    chess_player=[chess_player[_][0]  for _ in range(len(chess_player))]

    chess_player.remove(None)
    lichess_player.remove(None)


    a=isOnlineOnLichess(lichess_player, client)
    b=scrapeChessDotComOnlineStatus(chess_player)



    a['Time']=time
    b['Time']=time


    c.execute('''
          CREATE TABLE IF NOT EXISTS Online_lichess
          ([id] INTEGER PRIMARY KEY AUTOINCREMENT, [Time] TEXT,[Player] TEXT, [Online] TEXT)
          ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS Online_chessDotCom
        ([id] INTEGER PRIMARY KEY AUTOINCREMENT, [Time] TEXT,[Player] TEXT, [Online] TEXT)
        ''')
          
                        
    conn.commit()

    query_insert_online(a,'lichess')
    query_insert_online(b,'chessDotCom')


if __name__ == "__main__":
    while True:
        online('gekn')
        time.sleep(5)