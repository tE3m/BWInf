from regex import sub, search
from time import sleep
from util import saeubern
from nach import nach_laenge, nach_regex

def anpassen(lueckentext, worte):
    loesung = nach_laenge(lueckentext, worte)
    if loesung[1] != []:
        print("Regex")
        loesung = nach_regex(loesung[0], loesung[1], loesung[2])
    else:
        print("kein Regex")
    return loesung

print(anpassen(saeubern("_h __, _a_ __r ___e __b___!"), saeubern("arbeit eine für je oh was")))