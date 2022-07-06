

Progetto sviluppato a cura di Gadda Alberto, Guerini Rocco Paolo e Sauro Letterino
##################################################################################


Per lanciare le funzioni che iniziano a popolare il Database è sufficiente lanciare il file main.py

Dato che il main lavora su più thread, e a volte questo crea problemi con alcune versioni di python, è possibile lanciare singolarmente i 4 script che popolano il database:
    -player.py
    -rating.py
    -online.py
    -match.py

E' presente anche uno script sh che, se personalizzato con i giusti path, lancia queste funzioni in background (launch_all.sh)


Versione di Python utilizzata:
Python 3.8.12


Versione delle librerie utilizzate:
async-generator==1.10
async-timeout==3.0.1
berserk==0.10.0
chess.com==1.7.6
nest-asyncio==1.5.4
numpy==1.22.1
pandas==1.3.5
selenium==4.1.0
tqdm==4.62.3

Per utilizzare il codice di questo progetto è anche necessario avere installato ChromeDriver sul proprio PC.


