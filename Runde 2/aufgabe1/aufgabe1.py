from sys import argv, exit
import csv


class anmeldung:
    """Speichert eine Anmeldung"""
    beginntUm: int
    endetUm: int
    laenge: int
    dauer: int

    def __init__(self, beginntUm: int, endetUm: int, laenge: int):
        # Überprüft formale Gegebenheiten
        try:
            assert(beginntUm >= 8)
            assert(endetUm <= 18)
            assert(beginntUm < endetUm)
            assert(laenge != 0)
        # Beendet die Ausführung bei Fehlern
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
    """Findet einen Standort für eine gegebene Anmeldung."""
    global karte
    leereBereiche = []
    leererBereich = False
    # Findet unbelegte Bereiche mit der Größe der Registrierung oder größer
    for index, wert in enumerate(karte[registrierung.beginntUm]):
        if leererBereich == False:
            if wert == False:
                ersteStelle = index
                leererBereich = True
        if leererBereich == True:
            if wert != False:
                if index-ersteStelle >= registrierung.laenge:
                    leereBereiche.append([ersteStelle, index-1])
                    leererBereich = False
                else:
                    leererBereich = False
            elif index == len(karte[registrierung.beginntUm])-1:
                leereBereiche.append([ersteStelle, index])
    passt = []
    for bereich in leereBereiche:
        # Falls der gewählte Bereich größer ist als die benötigte Größe, werden alle möglichen Positionen innerhalb des Bereichs überprüft
        if bereich[1]+1-bereich[0] > registrierung.laenge:
            for start in range(bereich[0], bereich[1]+2-registrierung.laenge):
                luecke = [start, start+registrierung.laenge-1]
                for zeit in range(registrierung.beginntUm, registrierung.endetUm):
                    if karte[zeit][luecke[0]:luecke[1]+1] != [False for x in range(luecke[0], luecke[1]+1)]:
                        break
                    if zeit == registrierung.endetUm-1:
                        passt.append(luecke)
        # Falls nicht, kann der Bereich der passenden Größe direkt geprüft werden
        else:
            for zeit in range(registrierung.beginntUm, registrierung.endetUm):
                if karte[zeit][bereich[0]:bereich[1]+1] != [False for x in range(bereich[0], bereich[1]+1)]:
                    break
                if zeit == registrierung.endetUm-1:
                    return(bereich)
    # Wird kein exakt passender Bereich gefunden, wird die erste freie Lücke ausgegeben
    if passt != []:
        return(passt[0])
    # Wird überhaupt kein freier Bereich gefunden, wird False ausgegeben
    else:
        return False


def standZuordnen(standID: int, startposition: int):
    """Ordnet einen gegebenen Stand einer gegebenen Fläche zu"""
    global karte
    global anmeldungen
    stand: anmeldung = anmeldungen[standID]
    # Iteriert durch die stündlichen Zuordnungen und überschreibt die gegebenen Bereiche mit der gegebenen ID
    for anmeldezeit in range(stand.beginntUm, stand.endetUm):
        karte[anmeldezeit][startposition:startposition +
                           stand.laenge] = [standID for x in range(stand.laenge)]


# Zum Einlesen der Datei
f = open(argv[1], "r")
# Dient als Speicher für die Anmeldungen, mit einer eindeutigen Zahl als Schlüssel
anmeldungen = {}
# Dient als Speicher für die gewünschten Anfangszeitpunkte einer Anmeldung
beginntUm = {x: [] for x in range(8, 18)}
# Speichert die stündlichen Belegungen der Stellplätze
karte = {x: [False for x in range(0, 1000)] for x in range(8, 18)}
# Speichert die Sammlung aller akzeptierten Anmeldungen
akzeptiert = []
# Speicher die Einnahmen
gesamtsumme = 0
# Speicher die Anmeldungen, sortiert nach ihrem Wert (Länge * Dauer)
sortiert = []
# Liest jede Anmeldung ein, erstellt ein ´anmeldung´-Objekt in anmeldungen und trägt sie in ´beginntUm´ und ´sortiert´ ein
for zeile in range(1, int(f.readline())+1):
    werte = normen(f.readline())
    anmeldungen[zeile] = anmeldung(werte[0], werte[1], werte[2])
    beginntUm[werte[0]].append(zeile)
    sortiert.append(zeile)
f.close()
# Sortieren der Anmeldungen
sortiert.sort(
    key=lambda a: anmeldungen[a].laenge * anmeldungen[a].dauer, reverse=True)
for stand in sortiert:
    # Findet einen freien Stellplatz für den aktuellen ´stand´
    zugeordnet = platzFinden(anmeldungen[stand])
    # Falls ein Stellplatz gefunden wurde, kann die Anmeldung eingetragen werden
    if zugeordnet != False:
        standZuordnen(stand, zugeordnet[0])
        gesamtsumme += anmeldungen[stand].laenge * anmeldungen[stand].dauer
        akzeptiert.append(stand)
# Öffnen der Datei zur Ausgabe der Belegung
w = open("{}.csv".format(argv[1]), "w")
csvwriter = csv.writer(w)
# Schreiben der csv-Datei
for stunde in karte.values():
    csvwriter.writerow(stunde)
csvwriter.writerow(["Gesamt: " + str(gesamtsumme) + " Euro"])
w.close()
# Command-Line-Ausgabe
print("Die ausgewählten Anmeldungen befinden sich in den Zeilen",
      akzeptiert, ". Damit wird ein Umsatz von", gesamtsumme, "erzielt.")
