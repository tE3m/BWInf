from regex import sub, search

def saeubern(eingabe):
    """Macht aus einer Folge von mit Leerzeichen getrennten Worten eine Liste und löscht alle Satzzeichen."""
    eingabe = sub("[^\w\s_]", "", eingabe)
    eingabe = eingabe.split(" ")
    return eingabe

def tuple_zu_liste(eingabe):
    """Konvertiert einen Tuple zu einer Liste."""
    ausgabe = []
    for i in range(0, len(eingabe)):
        ausgabe.append(eingabe[i])
    return ausgabe

def finden(zufinden, finden_in):
    """Gibt die Stellen aus, an denen die beiden Strings die gleichen Buchstaben innehaben."""
    matches = []
    for i in range(0, len(zufinden)):
        if i<=len(finden_in)-1 and zufinden[i] == finden_in[i]:
            matches.append(i)
    return matches