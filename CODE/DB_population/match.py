from functions import games_chessDotCom, games_lichess, query_insert_match, add_opening
import berserk
import sqlite3


def match():
    test_database='/home/alberto/Desktop/database.db'
    conn = sqlite3.connect(test_database) 
    c = conn.cursor()  

    c.execute('''
          CREATE TABLE IF NOT EXISTS Match_lichess
          ([id] TEXT PRIMARY KEY, [white] TEXT,[whiteRate] INTEGER, [black] TEXT,[blackRate] INTEGER, [winner] TEXT, [speed] TEXT, [time] TEXT,[pgn] TEXT, [opening] TEXT)
          ''')

    c.execute('''
          CREATE TABLE IF NOT EXISTS Match_chessDotCom
          ([id] TEXT PRIMARY KEY, [white] TEXT,[whiteRate] INTEGER, [black] TEXT,[blackRate] INTEGER, [winner] TEXT, [speed] TEXT, [time] TEXT,[pgn] TEXT, [opening] TEXT)
          ''')
                            
    conn.commit()

    client = berserk.Client(session=berserk.TokenSession('lip_tASmazZwz0V835hoPxGH')) #Authentication in the Lichess API.

    query_old_li = "SELECT DISTINCT username_lichess FROM Player"

    old_li=c.execute(query_old_li).fetchall()
    old_li=[old_li[_][0]  for _ in range(len(old_li))]
    old_li.remove(None)

    query_old_ch = "SELECT DISTINCT username_chessDotCom FROM Player"

    old_ch=c.execute(query_old_ch).fetchall()
    old_ch=[old_ch[_][0]  for _ in range(len(old_ch))]
    old_ch.remove(None)


    query_white_li= "SELECT DISTINCT white FROM Match_lichess"
    query_black_li= "SELECT DISTINCT black FROM Match_lichess"

    white_li=c.execute(query_white_li).fetchall()
    white_li=[white_li[_][0]  for _ in range(len(white_li))]

    black_li=c.execute(query_black_li).fetchall()
    black_li=[black_li[_][0]  for _ in range(len(black_li))]

    players_li=list(set(white_li+black_li))


    query_white_ch= "SELECT DISTINCT white FROM Match_chessDotCom"
    query_black_ch= "SELECT DISTINCT black FROM Match_chessDotCom"

    white_ch=c.execute(query_white_ch).fetchall()
    white_ch=[white_ch[_][0]  for _ in range(len(white_ch))]

    black_ch=c.execute(query_black_ch).fetchall()
    black_ch=[black_ch[_][0]  for _ in range(len(black_ch))]

    players_ch=list(set(white_ch+black_ch))


    def_new_li=[]
    def_old_li=[]
    def_new_ch=[]
    def_old_ch=[]


    for i in old_li:
        if i in players_li:
            def_old_li.append(i)
        else:
            def_new_li.append(i)

    for i in old_ch:
        if i in players_ch:
            def_old_ch.append(i)
        else:
            def_new_ch.append(i)

    df_new_li=games_lichess(def_new_li, client, 0) #1
    df_new_ch=games_chessDotCom(def_new_ch, 0) #1


    df_old_li=games_lichess(def_old_li, client, 0)
    df_old_ch=games_chessDotCom(def_old_ch, 0)

    


    df_li=df_new_li.append(df_old_li, ignore_index=True)
    df_ch=df_new_ch.append(df_old_ch, ignore_index=True)


    df_li['pgn']=df_li['pgn'].apply(lambda x: str(x))
    df_li['time']=df_li['time'].apply(lambda x: x[:16])

    df_ch['pgn']=df_ch['pgn'].apply(lambda x: str(x))
    df_ch['time']=df_ch['time'].apply(lambda x: x[:16])

    df_li=add_opening(df_li)
    df_ch=add_opening(df_ch)

    query_insert_match(df_li, 'lichess')
    query_insert_match(df_ch, 'chessDotCom')


if __name__ == "__main__":
    match()