import debugpy

from copy import deepcopy

# Zum Einlesen von Kommandozeilenargumenten
import sys

# Normen der Daten


def normen(eingabe):
    """Trennt die einzelnen Elemente der Eingabe bei Leerzeichen"""
    eingabe = eingabe.strip(" \n").split(" ")
    try:
        for i in range(0, len(eingabe)):
            eingabe[i] = int(eingabe[i])
    finally:
        return eingabe


def fruchtliste(zuPruefen):
    """Fügt den Listen `fruechte` und `zuordnung` neue Früchte aus dem Argument hinzu, falls gegeben"""
    for frucht in zuPruefen:
        if frucht not in fruechte:
            fruechte.append(frucht)
            zuordnung.append([frucht, 0])


def zuordnen():
    """Ordnet den Früchten in `zuordnung` mögliche Schüsseln anhand der Überschneidungen der Früchte und Schüsseln
    bei den beobachteten Spießen zu. Falls eine eindeutige Zuordnung möglich ist, wird diese übernommen. Falls diese eindeutige
    Zuordnung lösungsrelevant ist, wird sie in die Lösung aufgenommen."""
    global zuordnung
    geloeste = []
    # Überprüfe jede Frucht
    for frucht in fruechte:
        # Initialisierung der Liste der Schüsseln, die in jedem Spieß vorkommen, in dem `frucht` auch vorkommt
        ueberschneidungen = []
        # Speichern der  Schüsseln der Spieße, in denen die Frucht vorhanden ist, in `ueberschneidungen`
        for spiess in spiesse:
            if frucht in spiess[1]:
                ueberschneidungen.append(spiess[0][:])
        # Da die Schüssel der Frucht in jedem Spieß vorkommen muss, kann man aus Effizienzgründen die Schüsseln
        # des kürzesten Spießes nehmen und überprüfen, welche Schüsseln dieses Spießes auch in jedem anderen Spieß aus
        # `ueberschneidungen` vorkommt
        nichtLoesung = []
        ueberschneidungen.sort(key=len)
        if ueberschneidungen != []:
            for schuessel in ueberschneidungen[0]:
                for schnitt in ueberschneidungen:
                    if schuessel not in schnitt:
                        nichtLoesung.append(schuessel)
                        break
            for element in nichtLoesung:
                ueberschneidungen[0].remove(element)
            # Falls es genau eine überall auftauchende Schüssel gibt, speicher das Paar aus Schüssel und
            # Frucht in `geloeste`
            if len(ueberschneidungen[0]) == 1:
                geloeste.append([ueberschneidungen[0][0], frucht])
                zuordnung = [[frucht, ueberschneidungen[0][0]]
                             if x[0] == frucht else x for x in zuordnung]
            else:
                zuordnung = [[frucht, ueberschneidungen[0]]
                             if x[0] == frucht else x for x in zuordnung]
    # Entferne die gelösten Paare aus den noch zu lösenden
    for geloest in geloeste:
        for zugeordnet in zuordnung:
            if type(zugeordnet[1])==list and geloest[0] in zugeordnet[1]:
                zugeordnet[1].remove(geloest[0])
                if len(zugeordnet[1])==1:
                    zugeordnet[1]=zugeordnet[1][0]
                    geloeste.append([zugeordnet[1], zugeordnet[0]])
        fruechte.remove(geloest[1])
        zuLoesen.remove(geloest[0])
        if geloest[1] in donald[1]:
            donald[0].append(geloest[0])
        


def eindeutig():
    """Ordnet den Früchten in `zuordnung` eindeutige Schüsseln zu"""
    for frucht in zuordnung:
        if len(donald[0])==len(donald[1]):
            break
        nichtMoegliche = []
        if type(frucht[1]) == list and len(frucht[1]) != 0:
            moegliche = frucht[1][:]
        elif type(frucht[1]) == int and frucht[1] == 0:
            moegliche = zuLoesen[:]
        else:
            continue
        for schuesseln in zuordnung:
            if schuesseln[0] != frucht[0]:
                if type(schuesseln[1]) == int and schuesseln[1] in moegliche:
                    frucht[1].remove(schuesseln[1])
                    moegliche.remove(schuesseln[1])
                    if schuesseln[1] in nichtMoegliche:
                        nichtMoegliche.remove(schuesseln[1])
                elif schuesseln[1] == moegliche:
                    # Falls eine andere Früchte exakt die selben möglichen Schüsseln haben und die Anzahl der Möglichkeiten
                    # der Anzahl der Früchte entspricht und dazu noch alle Früchte in der Lösung vorkommen,
                    # kann man diese Früchte als gelöst betrachten, da sie ohnehin alle gebraucht werden, also ist irrelevant,
                    # welche der Schüsseln tatsächlich zu der Frucht gehört
                    if len(moegliche)==2:
                            if (schuesseln[0] in donald[1] and frucht[0] in donald[1]) or (schuesseln[0] not in donald[1] and frucht[0] not in donald[1]):
                                if schuesseln[0] in donald[1] and frucht[0] in donald[1]:
                                    donald[0].append(moegliche[0])
                                    donald[0].append(moegliche[1])
                                frucht[1] = moegliche[0]
                                schuesseln[1] = moegliche[1]
                                fruechte.remove(frucht[0])
                                fruechte.remove(schuesseln[0])
                                zuLoesen.remove(moegliche[0])
                                zuLoesen.remove(moegliche[1])
                    else:
                        nichtLoesbar = []
                        inDonald = []
                        nichtInDonald = []
                        for paar in zuordnung:
                            if paar[1] == moegliche:
                                if paar[0] in donald[1]:
                                    inDonald.append(paar)
                                else:
                                    nichtInDonald.append(paar)
                        if len(nichtInDonald) == 0:
                            nichtLoesbar = inDonald
                        elif len(inDonald) == 0:
                            nichtLoesbar = nichtInDonald
                        if len(nichtLoesbar) == len(moegliche):
                            for moeglich in range(0, len(moegliche)):
                                nichtLoesbar[moeglich][1] = moegliche[moeglich]
                                fruechte.remove(nichtLoesbar[moeglich][0])
                                zuLoesen.remove(moegliche[moeglich])
                                if len(nichtInDonald) == 0:
                                    donald[0].append(moegliche[moeglich])
                            break
                elif type(schuesseln[1]) == list:
                    for schuessel in schuesseln[1]:
                        if schuessel in moegliche and schuessel in zuLoesen and schuessel not in nichtMoegliche:
                            nichtMoegliche.append(schuessel)

        if len(moegliche) > len(nichtMoegliche):
            for nichtMoeglich in nichtMoegliche:
                if nichtMoeglich in moegliche:
                    moegliche.remove(nichtMoeglich)

        if len(moegliche) == 1:
            frucht[1] = moegliche[0]
            fruechte.remove(frucht[0])
            zuLoesen.remove(moegliche[0])
            if frucht[0] in donald[1]:
                donald[0].append(moegliche[0])


# Einlesen der gegebenen Daten
f = open(sys.argv[1], "r")
zuLoesen = [x for x in range(1, int(f.readline())+1)]
# Speichern einer leeren Liste von Schüsselzahlen und der gesuchten Früchte in `donald`
donald = [[], normen(f.readline())]
# Speichern der Schüsselzahlen und Fruchtkombinationen der beobachteten Spieße in `spiesse`
spiesse = []
for i in range(0, int(f.readline())):
    spiesse.append([normen(f.readline()), normen(f.readline())])
# Schließen der eingelesenen Datei
f.close()
# Speichern der vorhandenen Früchte als Liste in `fruechte`
fruechte = []
# Speichern der Früchte und zugehörigen Schüsseln in `zuordnung`, mit 0 als Wert für
# ungelöste Schüsseln
zuordnung = []
fruchtliste(donald[1])
for spiess in spiesse:
    fruchtliste(spiess[1])
daten = [fruechte, zuordnung]
# Ruf `zuordnen` auf
zuordnen()
# Solange es noch ungelöste Paare gibt, rufe `eindeutig` auf
while len(donald[1]) != len(donald[0]):
    # Erstelle eine Kopie der Lösung für spätere Überprüfung
    daten_alt = deepcopy(daten)
    eindeutig()
    daten = [fruechte, zuordnung]
    # Wird nach einer vollständigen Iteration keine neue Lösung gefunden, dann gib die aktuelle aus, um eine
    # Endlosschleife zu verhindern
    if daten == daten_alt:
        print("Nicht geschafft")
        break
print(fruechte)
print(zuordnung)
print(donald)
