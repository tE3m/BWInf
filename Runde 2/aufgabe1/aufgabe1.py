from sys import argv, exit


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


def platzFinden(registrierung: anmeldung):
    global karte
    leereBereiche = []
    leererBereich = False
    for index, wert in enumerate(karte[registrierung.beginntUm]):
        if leererBereich == False:
            if wert == False:
                ersteStelle = index
                leererBereich = True
        if leererBereich == True:
            if index-ersteStelle+1 >= registrierung.laenge:
                if wert != False:
                    leereBereiche.append([ersteStelle, index-1])
                    leererBereich = False
                elif index == len(karte[registrierung.beginntUm])-1:
                    leereBereiche.append([ersteStelle, index])
    passt = []
    for bereich in leereBereiche:
        if bereich[1]+1-bereich[0] > registrierung.laenge:
            for start in range(bereich[0], bereich[1]+2-registrierung.laenge):
                luecke = [start, start+registrierung.laenge-1]
                for zeit in range(registrierung.beginntUm, registrierung.endetUm):
                    if karte[zeit][luecke[0]:luecke[1]+1] != [False for x in range(luecke[0], luecke[1]+1)]:
                        break
                    if zeit == registrierung.endetUm-1:
                        passt.append(luecke)
        else:
            return(bereich)
    if passt != []:    
        return(passt[0])
    else:
        return False


def standZuordnen(standID: int, startposition: int):
    global karte
    global anmeldungen
    stand: anmeldung = anmeldungen[standID]
    for anmeldezeit in range(stand.beginntUm, stand.endetUm):
        karte[anmeldezeit][startposition:startposition+stand.laenge] = [standID for x in range(stand.laenge)]

f = open(argv[1], "r")
anmeldungen = {}
beginntUm = {x: [] for x in range(8, 18)}
endetUm = {x: [] for x in range(9, 19)}
karte = {x: [False for x in range(0, 1000)] for x in range(8, 18)}
akzeptiert = []
gesamtsumme = 0
test = 0
sortiert = []
for zeile in range(1, int(f.readline())+1):
    werte = normen(f.readline())
    anmeldungen[zeile] = anmeldung(werte[0], werte[1], werte[2])
    beginntUm[werte[0]].append(zeile)
    endetUm[werte[1]].append(zeile)
    sortiert.append(zeile)
    test += (werte[1] - werte[0]) * werte[2]
sortiert.sort(key=lambda a: anmeldungen[a].laenge * anmeldungen[a].dauer, reverse=True)
for stand in sortiert:
    zugeordnet = platzFinden(anmeldungen[stand])
    if zugeordnet != False:
        standZuordnen(stand, zugeordnet[0])
        gesamtsumme += anmeldungen[stand].laenge * anmeldungen[stand].dauer
        akzeptiert.append(stand)
print("Die ausgewählten Anmeldungen befinden sich in den Zeilen", akzeptiert, ". Damit wird ein Umsatz von", gesamtsumme, "erzielt.")