from sys import argv

def normen(eingabe):
    """Trennt die einzelnen Elemente der Eingabe bei Leerzeichen"""
    eingabe = eingabe.strip(" \n").split(" ")
    try:
        for i in range(0, len(eingabe)):
            eingabe[i] = int(eingabe[i])
    finally:
        return eingabe

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