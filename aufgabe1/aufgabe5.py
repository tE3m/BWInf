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
                achieved_weight = combination.pop(0)
                weight_difference = achieved_weight - weight
                if weight_difference:
                    output += "{}g ({}g): {}\n".format(weight, weight_difference, combination)
                else:
                    output += "{}g: {}\n".format(weight, combination)
        return output

    @property
    def possible_weights(self) -> dict[int, list[int, list[int], list[int]]]:
        """The possible combinations for each weight between 10g and 10kg, in steps of 10g. Each side of the scale
        is represented by a list that contains the weights required.
        """
        for weight in self._possible_weights:
            self._possible_weights[weight] = self.find_combination(weight)
        return self._possible_weights

    def find_combination(self, weight: int) -> list[int, list[int], list[int]]:
        pass
