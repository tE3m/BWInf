from sys import argv, exit


class anmeldung:
    beginntUm: int
    endetUm: int
    laenge: int

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