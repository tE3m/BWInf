from sys import argv, exit
from math import ceil


def entfernung(ausgang, ziel):
    diff = ziel-ausgang
    if diff > 0:
        if diff < (umfang+1)/2:
            return (ziel-ausgang)
        else:
            return (ausgang+((umfang+1)-ziel))
    else:
        if abs(diff) < (umfang+1)/2:
            return abs(diff)
        else:
            return (ziel+((umfang+1)-ausgang))


def entfernungsliste(ausgang: int):
    global eisbuden
    entfernungen = []
    if index != 0:
        offset = 1
    else:
        offset = 0
    for haus in haeuser[int(index*(len(haeuser)-1)/eisbuden)+offset:int(eisbude*(len(haeuser)-1)/eisbuden)+1]:
        entfernungen.append(entfernung(ausgang, haus))
    entfernungen.sort()
    return entfernungen


def mehrheit(entfernungen: list):
    return sum(entfernungen[:ceil(len(entfernungen)/2)])


# Einlesen der gegebenen Datei
f = open(argv[1], "r")
# Einlesen der ersten Zeile
umfang, hausAnzahl = [int(x) for x in f.readline().strip("\n").split(" ")]
# Einlesen der Häuser
haeuser = [int(x) if int(
    x) <= umfang else "fehler" for x in f.readline().strip("\n").split(" ")]
f.close()
if len(haeuser) != hausAnzahl or "fehler" in haeuser:
    exit("Fehlerhafte Konfiguration.")

# Falls eine andere Anzahl als 3 Eisbuden gewünscht sind
try:
    eisbuden = int(argv[2])
except:
    eisbuden = 3

distanzen = []
adressen = [x for x in range(umfang)]
print(haeuser)
for index, eisbude in enumerate(range(1, eisbuden+1)):
    distanzen.append([])
    von = haeuser[int(index*(len(haeuser)-1)/eisbuden)]
    bis = haeuser[int(eisbude*(len(haeuser)-1)/eisbuden)]
    print(index, eisbude, von, bis)
    for adresse in adressen[von:bis]:
        if adresse in haeuser:
            continue
        cache = entfernungsliste(adresse)
        distanzen[index].append([adresse, cache, mehrheit(cache)])
    print(distanzen[index])
pass
