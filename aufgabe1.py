import sys
from regex import sub, search
from time import sleep

def normen(eingabe):
    """Macht aus einer Folge von mit Leerzeichen getrennten Worten eine Liste und löscht alle Satzzeichen."""
    eingabe = eingabe.split(" ")
    return eingabe

def finden(zufinden, finden_in):
    """Gibt die Stellen aus, an denen die beiden Strings die gleichen Buchstaben innehaben."""
    matches = []
    for i in range(0, len(zufinden)):
        if i<=len(finden_in)-1 and zufinden[i] == finden_in[i]:
            matches.append(i)
    return matches

def dopplung(liste):
    """Gleicht alle Elemente einer Liste mit sich selbst ab."""
    wahrheit = True
    for x in liste:
        for y in liste:
            if x != y:
                wahrheit = False
                break
        if wahrheit == False:
            break
    return wahrheit

def ersetzen(loesung, luecke, wort):
    zuersetzen = list(loesung[loesung.index(luecke)])
    wort = list(wort)
    print(zuersetzen)
    print(wort)
    zuersetzen = [wort[x] if x < len(wort) else zuersetzen[x] for x in range(0, len(zuersetzen))]
    loesung[loesung.index(luecke)] = "".join(zuersetzen)
    print(loesung)
    return loesung

def zuordnen(loesung, lueckentext, worte):
    """Ordnet Lücken ein Wort zu, wenn dieses die meisten übereinstimmenden Zeichen hat."""
    # Initialisierung der Liste der gelösten Stellen
    geloeste = []
    lueckentext_alt = lueckentext[:]
    for luecke in lueckentext:
        print(luecke)
        # Initalisierung der Liste der potenziell passenden Worte
        passend = []
        for wort in worte:
            # Die nachfolgenden Befehle sind nur relevant, wenn das Wort ohnehin so lang ist, wie
            if len(wort) == len(luecke) or len(wort)+1 == len(luecke):
                # Finde die Stellen heraus, an denen die aktuelle Lücke ´luecke´ und das aktuelle Wort ´wort´ gleich sind
                matches = finden(luecke, wort)
                # Ist die Liste der potenziell passenden Worte ´passend´ noch leer, oder hat das aktuelle Wort genau so viele 
                # Übereinstimmungen wie die bisherige potenzielle Lösung, füg das aktuelle Wort ´wort´ hinzu
                if len(passend)==0 or len(matches)==len(passend[-1][1]):
                    passend.append([wort, matches])
                # Hat es mehr Übereinstimmungen, überschreibe die bisherige potenzielle Lösung ´passend´ mit dem aktuellen Wort
                elif len(matches)>len(passend[-1][1]):
                    passend = [[wort, matches]]
        # Gibt es genau einen Eintrag in der Liste der potenziellen Lösungen ´passend´, ist dieser die Lösung
        if len(passend) == 1 or dopplung(passend):
            # Ersetze die Lücke in ´loesung´ mit dem gerade bestimmten Lösungspaar ´passend´
            print(passend[0][0])
            print(luecke)
            loesung = [passend[0][0] if x==luecke else x for x in loesung]
            #loesung = ersetzen(loesung, luecke, passend[0][0])
            # Hänge an die aktuelle Paar von ´luecke´ und ´wort´ an die Gelösten an
            geloeste.append([luecke, passend[0][0]])
    # Um die for-Schleifen intakt zu halten, werden die gelösten Stellen ´geloeste´ erst jetzt aus ihren Listen gelöscht
    for geloest in geloeste:
        lueckentext.remove(geloest[0])
        worte.remove(geloest[1])
    return [loesung, lueckentext, worte]

def kombinieren(lueckentext, worte):
    lueckentext = normen(lueckentext)
    worte = normen(worte)
    loesung = [lueckentext[:], lueckentext, worte]
    while loesung[1] != []:
        # Erstelle eine Kopie der Lösung für spätere Überprüfung
        loesung_alt = loesung[:]
        loesung = zuordnen(loesung[0], loesung[1], loesung[2])
        # Wird nach einer vollständigen Iteration keine neue Lösung gefunden, dann gib die aktuelle aus, um eine 
        # Endlosschleife zu verhindern
        print([loesung[0], loesung[1], loesung[2]])
        if loesung == loesung_alt:
            return " ".join(loesung[0])
    return " ".join(loesung[0])

if len(sys.argv)==2:
    f = open(sys.argv[1], "r")
    luecken = f.readline().strip("\n")
    worte = f.readline().strip("\n")
    print(kombinieren(luecken, worte))
    f.close()
else:
    print("Korrekte Nutzung: aufgabe1.py <Textdatei>")