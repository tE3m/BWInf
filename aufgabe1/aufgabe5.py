import sys
from bisect import bisect_left


class Scale:
    """A market scale scenario"""

    def __init__(self, path: str):
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
            if combination[0]:
                output += "{}g ({}g):\n    links:{}\n    rechts:{}\n".format(weight, -combination[0],
                                                                             combination[1], combination[2])
            else:
                output += "{}g:\n    links:{}\n    rechts:{}\n".format(weight, combination[1], combination[2])
        return output

    @property
    def possible_weights(self) -> dict[int, list[int, list[int], list[int]]]:
        """The possible combinations for each weight between 10g and 10kg, in steps of 10g. Each side of the scale
        is represented by a list that contains the weights required.
        """
        for weight in self._possible_weights:
            self._possible_weights[weight] = self.find_combination(weight)
        return self._possible_weights

    @staticmethod
    def remove_weight(weights: dict[int, int], to_remove: int):
        if to_remove not in weights.keys():
            raise ValueError
        weights[to_remove] -= 1
        if not weights[to_remove]:
            del weights[to_remove]

    def find_combination(self, weight: int, weights_copy: dict[int, int] = None,
                         current_combination: list[int, list[int], list[int]] = None) -> list[
                         int, list[int], list[int]]:
        """Attempts to find a combination of weights as close to the argument as possible."""
        if not current_combination:
            current_combination = [None, [], []]
        if weight > 0:
            weight_decrease = current_combination[1]
            weight_increase = current_combination[2]
        else:
            weight_decrease = current_combination[2]
            weight_increase = current_combination[1]
            weight *= -1
        if weights_copy is None:
            weights_copy = self.weights.copy()
        elif not weights_copy:
            current_combination[0] = weight
            return current_combination
        if weight in weights_copy.keys():
            current_combination[0] = 0
            weight_increase.append(weight)
            return current_combination
        min_difference: int = None
        difference_combination: list
        for right_weight in weights_copy.keys():
            for left_weight in weights_copy.keys():
                if left_weight == right_weight:
                    continue
                weight_difference = right_weight-left_weight
                if weight_difference == weight:
                    current_combination[0] = 0
                    weight_decrease.append(left_weight)
                    weight_increase.append(right_weight)
                    return current_combination
                if not min_difference or abs(weight - weight_difference) < abs(weight - min_difference):
                    min_difference = weight_difference
                    difference_combination = [left_weight, right_weight]
        weight_keys = [key for key in weights_copy]
        weight_keys_index = bisect_left(weight_keys, weight)
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
        else:
            current_combination[0] = weight
            return current_combination
        return self.find_combination(remaining_weight, weights_copy, current_combination)


if __name__ == '__main__':
    scale = Scale(sys.argv[1])
    print(scale)
