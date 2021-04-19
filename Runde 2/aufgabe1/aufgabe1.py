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
            if wert != False or index == len(karte[stunde])-1:
                leereBereiche.append([ersteStelle, index-1])
                leererBereich = False
    return leereBereiche


def standFinden(laenge: int, stunde: int, auswahl: dict = None, kombination: list = None):
    global anmeldungen
    if auswahl == None:
        auswahl = {distanz: [[x, anmeldungen[x].dauer] for x in beginntUm[stunde]
                             if anmeldungen[x].laenge == distanz] for distanz in range(1, laenge+1)}
        zuLoeschen = []
        [element[1].sort(key=itemgetter(1), reverse=True) if element[1] != [
        ] else zuLoeschen.append(element[0]) for element in auswahl.items()]
        for element in zuLoeschen:
            auswahl.pop(element)
        del zuLoeschen
    else:
        zuLoeschen = []
        for key in auswahl.keys():
            if key > laenge:
                zuLoeschen.append(key)
        for key in zuLoeschen:
            auswahl.pop(key)
    if kombination == None:
        kombination = []
    if auswahl == {}:
        return(kombination)
    kombination.append(auswahl[max(auswahl.keys())].pop(0)[0])
    if anmeldungen[kombination[-1]].laenge != laenge:
        if auswahl[max(auswahl.keys())] == []:
            auswahl.pop(max(auswahl.keys()))
        return(standFinden(laenge-anmeldungen[kombination[-1]].laenge, stunde, auswahl, kombination))
    return(kombination)


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