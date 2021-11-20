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
            if combination:
                if combination[0]:
                    output += "{}g ({}g):\n    links:{}\n    rechts:{}\n".format(weight, -combination[0],
                                                                                 combination[1], combination[2])
                else:
                    output += "{}g:    links:{}\n    rechts:{}\n".format(weight, combination[1], combination[2])
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
        if weights_copy is None:
            weights_copy = self.weights.copy()
        elif not weights_copy:
            current_combination[0] = weight
            return current_combination
        if weight in weights_copy.keys():
            current_combination[0] = 0
            current_combination[2].append(weight)
            return current_combination
        weight_keys = [key for key in weights_copy]
        weight_keys_index = bisect_left(weight_keys, weight)
        if not weight_keys_index:
            return current_combination
        max_weight = weight_keys[weight_keys_index - 1]
        self.remove_weight(weights_copy, max_weight)
        current_combination[2].append(max_weight)
        return self.find_combination(weight - max_weight, weights_copy, current_combination)
