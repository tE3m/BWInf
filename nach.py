from util import finden

def nach_laenge(lueckentext, worte):
    """Ordnet Lücken ein Wort zu, wenn eine eindeutige Zuordnung nach Länge möglich ist."""
    loesung = lueckentext
    geloeste = []
    while lueckentext != []:
        """Die Länge jeder Lücke wird mit der Länge jedes Wortes abgeglichen. Gibt es nur ein
        Wort mit gleich vielen Stellen wie die Lücke, gilt dieses als gelöst."""
        lueckentext_alt = lueckentext
        for luecke in lueckentext:
            passend = []
            for wort in worte:
                if len(wort) == len(luecke):
                    passend.append(wort)
            if len(passend) == 1:
                loesung = [passend[0] if x==luecke else x for x in loesung]
                geloeste.append([luecke, passend[0]])
        for geloest in geloeste:
            lueckentext.remove(geloest[0])
            worte.remove(geloest[1])
            """Wird nach einer vollständigen Iteration kein neues Paar gefunden, werden der 
            derzeitige Lösungsstand, die verbleibenden Lücken und verbleibenden Worte ausgegeben."""
        if lueckentext_alt == lueckentext:
            return [loesung, lueckentext, worte]

def nach_regex(loesung, lueckentext, worte):
    """Ordnet Lücken ein Wort zu, wenn eine eindeutige Zuordnung nach Länge möglich ist."""
    loesung = lueckentext
    geloeste = []
    while lueckentext != []:
        """Die übereinstimmenden Stellen zwischen Lücke und Wort wird überprüft. Das Wort mit den meisten
        übereinstimmenden Stellen wird als die Lösung angesegen."""
        lueckentext_alt = lueckentext
        for luecke in lueckentext:
            passend = []
            print("\n" + luecke + "\n")
            for wort in worte:
                print(wort)
                matches = finden(luecke, wort)
                print(passend, matches)
                if len(matches)==len(passend):
                    passend.append(wort)
                elif len(matches)>len(passend):
                    passend = [wort]
            print(passend)
            if len(passend) == 1:
                loesung = [passend[0] if x==luecke else x for x in loesung]
                geloeste.append([luecke, passend[0]])
        for geloest in geloeste:
            print(geloest[0], geloest[1], lueckentext, worte)
            lueckentext.remove(geloest[0])
            worte.remove(geloest[1])
        print(loesung)
        """Wird nach einer vollständigen Iteration kein neues Paar gefunden, werden der 
        derzeitige Lösungsstand, die verbleibenden Lücken und verbleibenden Worte ausgegeben."""
        if lueckentext_alt == lueckentext:
            return [loesung, lueckentext, worte]