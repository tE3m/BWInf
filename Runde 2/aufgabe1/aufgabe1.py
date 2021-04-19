from sys import argv, exit
from operator import itemgetter


class anmeldung:
    beginntUm: int
    endetUm: int
    laenge: int
    dauer: int

    def __init__(self, beginntUm: int, endetUm: int, laenge: int):
        try:
            assert(beginntUm >= 8)
            assert(endetUm <= 18)
            assert(beginntUm < endetUm)
            assert(laenge != 0)
        except AssertionError:
            print("Die Konfiguration", beginntUm,
                  endetUm, laenge, "ist ungültig.")
            exit()
        self.beginntUm = beginntUm
        self.endetUm = endetUm
        self.laenge = laenge
        self.dauer = endetUm-beginntUm


def normen(eingabe):
    """Trennt die einzelnen Elemente der Eingabe bei Leerzeichen"""
    eingabe = eingabe.strip(" \n").split(" ")
    try:
        for i in range(0, len(eingabe)):
            eingabe[i] = int(eingabe[i])
    finally:
        return eingabe


def platzFinden(stunde: int):
    global karte
    leereBereiche = []
    leererBereich = False
    for index, wert in enumerate(karte[stunde]):
        if leererBereich ==False:
            if wert == False:
                ersteStelle = index
                leererBereich = True
        if leererBereich == True:
            if wert != False:
                leereBereiche.append([ersteStelle, index-1])
                leererBereich = False
            elif index == len(karte[stunde])-1:
                leereBereiche.append([ersteStelle, index])
    return leereBereiche


def standFinden(laenge: int, stunde: int, auswahl: list = None, kombination: list = None):
    global anmeldungen
    if auswahl == None:
        auswahl = [x for x in beginntUm[stunde]
                   if anmeldungen[x].laenge <= laenge]
        auswahl.sort(key=lambda a: anmeldungen[a].laenge * anmeldungen[a].dauer, reverse=True)
    else:
        auswahl = list(filter(lambda a: anmeldungen[a].laenge <= laenge, auswahl))
    if kombination == None:
        kombination = []
    if auswahl == []:
        return(kombination)
    kombination.append(auswahl.pop(0))
    beginntUm[stunde].remove(kombination[-1])
    if anmeldungen[kombination[-1]].laenge <= laenge:
        return(standFinden(laenge-anmeldungen[kombination[-1]].laenge, stunde, auswahl, kombination))
    return(kombination)


def standZuordnen(standID: int, startposition: int):
    global karte
    global anmeldungen
    stand: anmeldung = anmeldungen[standID]
    for anmeldezeit in range(stand.beginntUm, stand.endetUm):
        karte[anmeldezeit][startposition:startposition+stand.laenge] = [standID for x in range(stand.laenge)]

f = open(argv[1], "r")
anmeldungen = {}
beginntUm = {}
endetUm = {}
karte = [False for x in range(0, 1000)]
for zeile in range(0, int(f.readline())):
    anmeldung = normen(f.readline())
    anmeldungen[zeile] = anmeldung
    if anmeldung[0] not in beginntUm.keys():
        beginntUm[anmeldung[0]] = [zeile]
    else:
        beginntUm[anmeldung[0]].append(zeile)
    if anmeldung[1] not in endetUm.keys():
        endetUm[anmeldung[1]] = [zeile]
    else:
        endetUm[anmeldung[1]].append(zeile)
pass