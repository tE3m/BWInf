from copy import deepcopy

# Zum Einlesen von Kommandozeilenargumenten
from sys import argv, exit


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
            zuordnung[frucht] = 0


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
        kuerzesterSpiess = []
        if ueberschneidungen != []:
            kuerzesterSpiess = min(ueberschneidungen)
            if len(ueberschneidungen) != 1:
                ueberschneidungen.remove(kuerzesterSpiess)
                for schuessel in kuerzesterSpiess:
                    for schnitt in ueberschneidungen:
                        if schuessel not in schnitt:
                            nichtLoesung.append(schuessel)
                            break
                kuerzesterSpiess = [
                    x for x in kuerzesterSpiess if x not in nichtLoesung]
            # Falls es genau eine überall auftauchende Schüssel gibt, speicher das Paar aus Schüssel und
            # Frucht in `geloeste`
            if len(kuerzesterSpiess) == 1:
                geloeste.append([frucht, kuerzesterSpiess[0]])
                zuordnung[frucht] = kuerzesterSpiess[0]
            elif kuerzesterSpiess != []:
                zuordnung[frucht] = kuerzesterSpiess
            else:
                zuordnung[frucht] = nichtLoesung
    # Entferne die gelösten Paare aus den noch zu lösenden
    for geloest in geloeste:
        for zugeordnet in zuordnung.keys():
            if type(zuordnung[zugeordnet]) == list and geloest[1] in zuordnung[zugeordnet]:
                zuordnung[zugeordnet].remove(geloest[1])
                if len(zuordnung[zugeordnet]) == 1:
                    zuordnung[zugeordnet] = zuordnung[zugeordnet][0]
                    geloeste.append([zugeordnet, zuordnung[zugeordnet]])
        fruechte.remove(geloest[0])
        zuLoesen.remove(geloest[1])
        if geloest[0] in donald[1]:
            donald[0].append(geloest[1])


def eindeutig():
    """Ordnet den Früchten in `zuordnung` eindeutige Schüsseln zu"""
    for frucht in zuordnung.keys():
        # Ist die Lösung gefunden, kann die Schleife abgebrochen werden
        if len(donald[0]) == len(donald[1]):
            break
        nichtMoegliche = []
        # Wurde noch keine eindeutige Lösung gefunden, wird eine Kopie des derzeitigen Standes erstellt
        if type(zuordnung[frucht]) == list and len(zuordnung[frucht]) != 0:
            moegliche = zuordnung[frucht][:]
        # Kommt die Frucht auf keinem Spieß vor, muss nach dem Ausschlussverfahren vorgegangen werden
        elif type(zuordnung[frucht]) == int and zuordnung[frucht] == 0:
            moegliche = zuLoesen[:]
        # Ist die Frucht bereits gelöst, muss nichts getan werden
        else:
            continue
        # Iteration Vergleich mit allen Früchten
        for schuesseln in zuordnung.items():
            # (Außer sich selbst)
            if schuesseln[0] != frucht:
                # Ist die verglichene Frucht bereits gelöst, kann die Schüssel aus den Möglichen entfernt werden
                if type(schuesseln[1]) == int and schuesseln[1] in moegliche:
                    zuordnung[frucht].remove(schuesseln[1])
                    moegliche.remove(schuesseln[1])
                    if schuesseln[1] in nichtMoegliche:
                        nichtMoegliche.remove(schuesseln[1])
                elif schuesseln[1] == moegliche:
                    # Falls eine andere Früchte exakt die selben möglichen Schüsseln haben und die Anzahl der Möglichkeiten
                    # der Anzahl der Früchte entspricht und dazu noch alle Früchte in der Lösung vorkommen,
                    # kann man diese Früchte als gelöst betrachten, da sie ohnehin alle gebraucht werden, also ist irrelevant,
                    # welche der Schüsseln tatsächlich zu der Frucht gehört
                    if len(moegliche) == 2:
                        if (schuesseln[0] in donald[1] and frucht in donald[1]) or (schuesseln[0] not in donald[1] and frucht not in donald[1]):
                            if schuesseln[0] in donald[1] and frucht in donald[1]:
                                donald[0].append(moegliche[0])
                                donald[0].append(moegliche[1])
                            zuordnung[frucht] = moegliche[0]
                            zuordnung[schuesseln[0]] = moegliche[1]
                            fruechte.remove(frucht)
                            fruechte.remove(schuesseln[0])
                            zuLoesen.remove(moegliche[0])
                            zuLoesen.remove(moegliche[1])
                    else:
                        # Sind nicht bloß zwei Früchte involviert, müssen alle Früchte mit diesem Lösungsstand betrachtet werden
                        nichtLoesbar = []
                        inDonald = []
                        nichtInDonald = []
                        for paar in zuordnung.items():
                            if paar[1] == moegliche:
                                if paar[0] in donald[1]:
                                    inDonald.append(paar)
                                else:
                                    nichtInDonald.append(paar)
                        # Es kann lediglich eine Aussage getroffen werden, wenn alle oder keine der Früchte für die Lösung gebraucht wird
                        if len(nichtInDonald) == 0:
                            nichtLoesbar = inDonald
                        elif len(inDonald) == 0:
                            nichtLoesbar = nichtInDonald
                        # Ist das der Fall, können alle involvierten Früchte als gelöst betrachtet werden
                        if len(nichtLoesbar) == len(moegliche):
                            for moeglich in range(0, len(moegliche)):
                                zuordnung[nichtLoesbar[moeglich]    #AutoPEP8 möchte es so formatiert
                                          [0]] = moegliche[moeglich]
                                fruechte.remove(nichtLoesbar[moeglich][0])
                                zuLoesen.remove(moegliche[moeglich])
                                if len(nichtInDonald) == 0:
                                    donald[0].append(moegliche[moeglich])
                            break
                # Ist die verglichene Frucht einfach nur unglöst, können die möglichen Schüsseln auf Einzigartigkeit überprüft werden
                elif type(schuesseln[1]) == list:
                    for schuessel in schuesseln[1]:
                        if schuessel in moegliche and schuessel in zuLoesen and schuessel not in nichtMoegliche:
                            nichtMoegliche.append(schuessel)

        # Konnte ein Teil der möglichen Lösung so ausgeschlossen werden, wird sie gelöscht
        if len(moegliche) > len(nichtMoegliche):
            for nichtMoeglich in nichtMoegliche:
                moegliche.remove(nichtMoeglich)

        # Ist die Lösung auf eine Möglichkeit reduziert worden, muss dies die Lösung sein
        if len(moegliche) == 1:
            zuordnung[frucht] = moegliche[0]
            fruechte.remove(frucht)
            zuLoesen.remove(moegliche[0])
            if frucht in donald[1]:
                donald[0].append(moegliche[0])

        # Konnte die mögliche Lösung für diese eingeschränkt werden, gilt diese auch für die anderen Früchte mit der gleichen potenziellen Lösung
        elif type(zuordnung[frucht]) == list and len(moegliche) < len(zuordnung[frucht]):
            if len(nichtLoesbar) != 0:
                for nichtLoesbare in nichtLoesbar:
                    zuordnung[nichtLoesbare[0]] = moegliche


# Einlesen der gegebenen Daten
f = open(argv[1], "r")
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
zuordnung = {}
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
        print("Von gesuchten", len(donald[1]), "Fruchtsorten wurden folgende", len(donald[0]), "Schüsseln bestimmt:", donald[0])
        print("Die restliche Zuordnung wurde wie folgt bestimmt:", zuordnung)
        exit()
print("Als gesuchte Schüsseln wurden", donald[0], "identifiziert.")
