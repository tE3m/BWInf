import sys
from random import random, shuffle
from math import log


def einlesen(anzahl):
    """Liest die Spielstärken ein."""
    # Initialisierung der Liste der Spielstärken ´spieler´
    spieler = []
    # Lies jede Spielstärke ein und speichere jede Spielstärke als ´int´ in ´spieler´
    for i in range(0, anzahl):
        spieler.append(int(f.readline().strip("\n")))
    return spieler


def liga(spieler):
    """Simuliert ein Turnier im Liga-System"""
    # Initialisierung der Liste der Sieger, da in einer Liga mehrere Spieler gewinnen können
    sieger = []
    for mitlauf in range(0, len(spieler)):
        # Erstell für jeden Spieler eine Liste bestehend aus Spielstärke und Siegen
        spieler[mitlauf] = [spieler[mitlauf], 0]
    # Iteriere jedes Element gegen jedes andere Element
    for i in range(0, len(spieler)):
        for j in range(0, len(spieler)):
            # Der Spieler spielt nicht gegen sich selbst
            if i != j:
                # Ist die Spielstärke eines Spielers ´0´, dann kann dies automatisch als Sieg für
                # den Gegner gewertet werden
                if spieler[j][0] != 0.0 and spieler[j][0] != 0.0:
                    # Erzeuge eine pseudozufällige Zahl
                    zahl = random()
                    # Ist diese kleiner als der Quotient aus der ersten Spielstärke und der Summe
                    # der Spielstärken, werte dies als einen Sieg für den ersten Spieler
                    if zahl < spieler[i][0]/(spieler[i][0]+spieler[j][0]):
                        spieler[i][1] += 1
                    # Sonst, werte dies als Sieg für den zweiten Spieler
                    else:
                        spieler[j][1] += 1
                elif spieler[j][0] == 0.0:
                    spieler[i][1] += 1
                else:
                    spieler[j][1] += 1
    # Ab hier wird nur noch die Anzahl der Siege benötigt, also wird an jedem Index in ´spieler´
    # nur noch diese gespeichert
    for i in range(0, len(spieler)):
        spieler[i] = spieler[i][1]
    # In ´sieger´ werden alle Indizes gespeichert, an denen die Siege am höchsten sind
    for i, j in enumerate(spieler):
        if j == max(spieler):
            sieger.append(i)
    return sieger


def ko(spieler):
    """Simuliert ein Turnier im K.O.-System"""
    # Initialisierung der Liste der für die nächsten Runde qualifizierten Indizes
    qualifiziert = []
    # Speichere so viele Indizes, wie es Spieler gibt
    for i in range(0, len(spieler)):
        qualifiziert.append(i)
    # Ändere die Reihenfolge der Indizes zu einer zufälligen Abfolge
    shuffle(qualifiziert)
    # Die Anzahl der Runden beträgt in einem K.O.-System immer den Logarithmus
    # zur Basis 2 der Spielerzahl, daher werden so viele Runden simuliert
    for runden in range(0, int(log(len(spieler), 2))):
        # Die Anzahl der Paarungen ist immer halb so hoch wie die Anzahl der Spieler
        for mitlauf in range(0, int(len(qualifiziert)/2)):
            # Die Paarung besteht aus dem Spieler an der Stelle der Mitlaufvariable
            # ´mitlauf´ und dem an der nächsten Stelle
            spielende = [spieler[qualifiziert[mitlauf]],
                         spieler[qualifiziert[mitlauf+1]]]
            # Ist die Spielstärke eines Spielers ´0´, dann kann dies automatisch als Sieg für
            # den Gegner gewertet werden
            if spielende[1] != 0.0 and spielende[0] != 0:
                # Erzeuge eine pseudozufällige Zahl
                zahl = random()
                # Ist diese kleiner als der Quotient aus der ersten Spielstärke und der Summe
                # der Spielstärken, werte dies als einen Sieg für den ersten Spieler
                if zahl < spielende[0]/(spielende[0]+spielende[1]):
                    # Lösche das Element des Verlierers, wodurch die for-Schleife an die richtige Stelle springt
                    del qualifiziert[mitlauf+1]
                # Sonst, werte dies als Sieg für den zweiten Spieler
                else:
                    del qualifiziert[mitlauf]
            elif spielende[0] == 0:
                del qualifiziert[mitlauf]
            else:
                del qualifiziert[mitlauf+1]
    return([qualifiziert[0]])


def ko5(spieler):
    """Genau wie ´ko´, bloß mit 5 Spielen pro Paarung"""
    qualifiziert = []
    for i in range(0, len(spieler)):
        qualifiziert.append(i)
    shuffle(qualifiziert)
    for runden in range(0, int(log(len(spieler), 2))):
        for mitlauf in range(0, int(len(qualifiziert)/2)):
            spielende = [spieler[qualifiziert[mitlauf]],
                         spieler[qualifiziert[mitlauf+1]]]
            # Initialisierung der Siege der Paarung, der Index entspricht
            # dem Index des Spielers in ´spielende´
            siege = [0, 0]
            if spielende[1] != 0.0 and spielende[0] != 0:
                # Die Spielstärken bestreiten 5 'Spiele' gegeneinander, bevor ein
                # Sieger ernannt wird
                for spiele in range(0, 5):
                    if spielende[1] != 0.0 and spielende[0] != 0:
                        zahl = random()
                        if zahl < spielende[0]/(spielende[0]+spielende[1]):
                            siege[0] += 1
                        else:
                            siege[1] += 1
            elif spielende[0] == 0:
                siege[1] = 1
            else:
                siege[0] = 1
            # Nun wird die Liste umgekehrt, da im Falle eines Sieges von Index 1
            # nichts zu ´mitlauf´ beim Entfernen addiert werden soll, umgekehrt
            # bei einem Sieg von Index 0
            siege.reverse()
            del qualifiziert[mitlauf+siege.index(max(siege))]
    return([qualifiziert[0]])


def wiederholung(wiederholungen, func):
    """Wiederholt ´func´ ´wiederholungen´ mal."""
    # Die Datei ´f´ wird global gebraucht
    global f
    # Öffne die Datei der Spielstärken
    f = open(sys.argv[1], "r")
    # Die Anzahl der Spieler ist in der ersten Zeile der Datei definiert
    spieler = int(f.readline().strip("\n"))
    # Kopiere die verfügbaren Funktionen in ´funktionen´
    funktionen = globals().copy()
    funktionen.update(locals())
    # Die aufzurufende Funktion ´func´ befindet sich in ´funktionen´
    func = funktionen.get(func)
    # Initialisierung der Liste der Anzahl der Siege
    siege = []
    # Lies die Spielstärken durch Aufrufen von ´einlesen´ auf
    spielende = einlesen(spieler)
    # IO-Operationen sind beendet
    f.close()
    # Kopiere ´spielende´ für einen späteren Vergleich
    spielende_kopie = spielende[:]
    print(spielende)
    # Initialisierung der Siege der Paarung, der Index entspricht
    # dem Index des Spielers in ´spielende´
    for i in range(0, spieler):
        siege.append(0)
    # Rufe ´func´ ´wiederholungen´ mal auf
    for i in range(0, wiederholungen):
        # Speichere den Sieger dieser Iteration in ´sieger´
        sieger = func(spielende)
        # Erhöhe die Anzahl der Siege dieser Sieger in ´siege´
        for j in range(0, len(sieger)):
            siege[sieger[j]] += 1
    # Initialisierung der Liste der auszugebenden Sieger
    ausgabe = []
    # In ´ausgabe´ werden alle Indizes gespeichert, an denen die Siege am höchsten sind
    for i, j in enumerate(siege):
        if j == max(siege):
            ausgabe.append(spielende_kopie[i])
    print(siege)
    return ausgabe


if len(sys.argv) == 4:
    print(wiederholung(int(sys.argv[2]), sys.argv[3]))
else:
    print("Korrekte Nutzung: aufgabe3.py <Datei>.txt <Wiederholungen> <liga|ko|ko5>")
