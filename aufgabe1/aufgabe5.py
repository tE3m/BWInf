# Wird importiert, um die Datei mit Daten als Argument einlesen zu können
import sys
# Wird importiert, um die binäre Suche in einer Liste verfügbar zu haben
from bisect import bisect_left


class Scale:
    """Ein Szenario für eine Marktwaage"""

    def __init__(self, path: str):
        # Initialisierung aller Attribute
        self.weights: dict[int, int] = {}
        self._possible_weights = {weight: None for weight in range(10, 10010, 10)}
        with open(path, "r") as file:
            for line in range(int(file.readline())):
                weight, amount = file.readline().split(" ")
                self.weights[int(weight)] = int(amount)

    def __repr__(self) -> str:
        return "Scale(" + str(self.weights) + ")"

    def __str__(self) -> str:
        output = ""
        for index, item in enumerate(self.possible_weights.items()):
            weight, combination = item
            if combination[0] > 0:
                combination[0] = "+" + str(combination[0])
            if combination[0]:
                output += "{}g ({}g):\n    links:{}\n    rechts:{}\n".format(weight, combination[0],
                                                                             combination[1], combination[2])
            else:
                output += "{}g:\n    links:{}\n    rechts:{}\n".format(weight, combination[1], combination[2])
        return output

    @property
    def possible_weights(self) -> dict[int, list[int, list[int], list[int]]]:
        """Die möglichen Kombinationen für jedes Gewicht zwischen 10g und 10kg, in Schritten von 10g. Jede Seite der
        Waage wird durch eine Liste dargestellt, die die erforderlichen Gewichte enthält.
        :returns: `dict` mit den Lösungen für jedes Gewicht
        """
        for weight in self._possible_weights:
            self._possible_weights[weight] = self.find_combination(weight)
        return self._possible_weights

    @staticmethod
    def remove_weight(weights: dict[int, int], to_remove: int) -> None:
        """Entfernt das übergebene Gewicht `to_remove` aus der Sammlung der Gewichte `weights`
        :param weights: Ansammlung von Gewichten als `dict`
        :param to_remove: Gewicht, das aus `weights` entfernt werden soll
        """
        if to_remove not in weights.keys():
            raise ValueError
        weights[to_remove] -= 1
        if not weights[to_remove]:
            del weights[to_remove]

    def find_combination(self, weight: int, weights_copy: dict[int, int] = None,
                         current_combination: list[int, list[int], list[int]] = None) -> list[
                         int, list[int], list[int]]:
        """Findet rekursiv eine Kombination an Gewichten, die so nah wie möglich am übergebenen Gewicht
        `weight` dran liegt
        :param weight: gesuchtes Gewicht
        :param weights_copy: `dict` mit Gewichten, mit denen gearbeitet wird
        :param current_combination: Mitlaufwert für Rekursion
        :return: Eine Liste, die die Differenz zum übergebenen Gewicht und die Gewichte rechts und links enthält"""
        if not current_combination:
            current_combination = [None, [], []]
        # Falls `weight` negativ ist, werden die Seiten der Waage vertauscht
        if weight > 0:
            weight_decrease = current_combination[1]
            weight_increase = current_combination[2]
            weight_factor = 1
        else:
            weight_decrease = current_combination[2]
            weight_increase = current_combination[1]
            weight *= -1
            weight_factor = -1
        # Falls es noch kein `dict` mit Gewichten gibt, kopiere das des Objekts
        if weights_copy is None:
            weights_copy = self.weights.copy()
        # Gibt es keine Gewichte mehr, kann keine Lösung gefunden werden
        elif not weights_copy:
            current_combination[0] = weight * weight_factor
            return current_combination
        # Ist das gesuchte Gewicht darstellbar als ein einziges Gewichtsstück, kann dieses als Lösung zurückgegeben
        # werden
        if weight in weights_copy.keys():
            current_combination[0] = 0
            weight_increase.append(weight)
            return current_combination
        # Ist das nicht der Fall, werden alle Kombinationen der vorhandenen Gewichte durchgespielt und die Kombination
        # mit dem geringsten Abstand zum gesuchten Gewicht wird in `difference_combination` gespeichert
        min_difference: int = None
        difference_combination: list
        for right_weight in weights_copy.keys():
            for left_weight in weights_copy.keys():
                if left_weight == right_weight:
                    continue
                weight_difference = right_weight-left_weight
                # Entspricht eine Kombination exakt dem gesuchten Gewicht, kann diese bereits früher als Lösung
                # zurückgegeben werden
                if weight_difference == weight:
                    current_combination[0] = 0
                    weight_decrease.append(left_weight)
                    weight_increase.append(right_weight)
                    return current_combination
                if not min_difference or abs(weight - weight_difference) < abs(weight - min_difference):
                    min_difference = weight_difference
                    difference_combination = [left_weight, right_weight]
        # Findet das größte einzelne vorhandene Gewicht, das kleiner als das gesuchte ist
        weight_keys = [key for key in weights_copy]
        weight_keys_index = bisect_left(weight_keys, weight)
        # Je nachdem, ob das einzelne Gewicht oder die Kombination aus zweien näher am gesuchten Gewicht liegen,
        # wird das eine oder das andere gewählt, um fortzufahren
        if weight_keys_index and min_difference and abs(weight-weight_keys[weight_keys_index - 1]) <=\
                abs(weight-min_difference) or weight_keys_index and not min_difference:
            max_weight = weight_keys[weight_keys_index - 1]
            self.remove_weight(weights_copy, max_weight)
            weight_increase.append(max_weight)
            remaining_weight = weight - max_weight
        elif min_difference and abs(weight-min_difference) < weight:
            self.remove_weight(weights_copy, difference_combination[0])
            self.remove_weight(weights_copy, difference_combination[1])
            weight_decrease.append(difference_combination[0])
            weight_increase.append(difference_combination[1])
            remaining_weight = weight - min_difference
        # Nähert keiner der beiden Ansätze sich der Lösung, kann keine bessere Lösung gefunden werden
        else:
            current_combination[0] = weight * weight_factor
            return current_combination
        # Rekursion, falls noch Gewicht verbleibt
        return self.find_combination(remaining_weight, weights_copy, current_combination)


if __name__ == '__main__':
    scale = Scale(sys.argv[1])
    print(scale)
