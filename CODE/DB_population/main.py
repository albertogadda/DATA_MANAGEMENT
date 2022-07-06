import time
import datetime
from online import online
from player import player
from rating import rating
from match import match
import threading
import nest_asyncio
nest_asyncio.apply() 

def f_player_rating():
    while True:
        now=time.time()
        player()
        rating()
        time.sleep(3600-(time.time()-now))  #eseguo questa funzione una volta ogni ora

def f_online():
    while True:
        now=time.time()
        online()
        time.sleep(600-(time.time()-now))   #eseguo questa funzione una volta ogni 10 minuti

def f_match():
    while True:
        now=time.time()
        match()
        time.sleep(86400-(time.time()-now)) #eseguo questa funzione una volta al giorno



if __name__ == "__main__":
    t1=threading.Thread(target = f_player_rating)
    t1.start()

    time.sleep(600) #aspetto che si popoli la tabella dei player, dato che è l'input delle altre funzioni

    t2=threading.Thread(target = f_online)
    t2.start()

    t3=threading.Thread(target = f_match)
    t3.start()

