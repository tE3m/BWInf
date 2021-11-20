from sys import argv
from string import ascii_uppercase as letters
from copy import deepcopy as dc
from typing import Union
from colorama import Fore
from collections import ChainMap


def get_index_of_letter(letter: str) -> int:
    return letters.index(letter)


def get_letter_at_index(index: int) -> str:
    return letters[index]


class ParkingLot:

    def __init__(self, path: str) -> None:
        self.normal_cars = []
        self._sideways_cars = []
        self._blocked_spots = {}
        with open(path, "r") as file:
            max_letter = file.readline()[2]
            for normal_car_letter in letters[:get_index_of_letter(max_letter) + 1]:
                self.normal_cars.append(NormalCar(self, normal_car_letter))
            for sideways_car in range(int(file.readline())):
                sideways_car_letter, position = file.readline().split()
                self._sideways_cars.append(SideWaysCar(self, sideways_car_letter, int(position)))

    def __str__(self) -> str:
        solution = self.solution
        output = ""
        for slot in solution:
            if solution[slot] is False:
                output += slot + ": nicht lösbar\n"
            else:
                output += slot + ": "
                for index, item in enumerate(reversed(solution[slot].items())):
                    blocking_car, move = item
                    if move > 0:
                        direction = "rechts"
                    else:
                        direction = "links"
                    output += blocking_car + " " + str(abs(move)) + " " + direction
                    if index != len(solution[slot]) - 1:
                        output += ", "
                output += "\n"
        return output

    @property
    def blocked_spots(self) -> list:
        return sum(list(self._blocked_spots.values()), [])

    def update_blocked_spots(self, car=None) -> None:
        if car is None:
            for blocking_car in self._blocked_spots:
                self._blocked_spots[blocking_car] = [blocking_car.position, blocking_car.position + 1]
        elif car.position in self.blocked_spots and self.find_blocking_car(
                car.position) != car or car.position + 1 in self.blocked_spots and self.find_blocking_car(
            car.position + 1) != car:
            raise ValueError("Dieser Platz ist bereits belegt.")
        else:
            self._blocked_spots[car] = [car.position, car.position + 1]

    def find_blocking_car(self, position: int):
        return self._sideways_cars[int(self.blocked_spots.index(position) / 2)]

    @property
    def solution(self) -> dict:
        solution_dict = {}
        for normal_car in self.normal_cars:
            if not normal_car.is_movable:
                solution_dict[normal_car.letter] = self.find_solution(normal_car.position)
            else:
                solution_dict[normal_car.letter] = {}
        return solution_dict

    def find_solution(self, position: int, steps: ChainMap = None) -> Union[dict, bool]:
        if steps is None:
            steps = ChainMap()
        if position not in range(len(self.normal_cars)) or position in self.blocked_spots and self.find_blocking_car(
                position).letter in steps.keys():
            return False
        elif position in self.blocked_spots:
            parking_lot_copy = dc(self)
            blocking_car = parking_lot_copy.find_blocking_car(position)
            position_difference = position - blocking_car.position
            if position_difference == 1:
                disposition = -1
            else:
                disposition = 1
            if not blocking_car.is_movable(disposition):
                if disposition == -1:
                    disposition = 2
                else:
                    disposition = -2
            if blocking_car.is_movable(disposition):
                blocking_car.position += disposition
                steps = steps.new_child({blocking_car.letter: disposition})
            else:
                steps = steps.new_child({blocking_car.letter: 0})
                steps_right = parking_lot_copy.find_solution(blocking_car.position + 2 + position_difference, dc(steps))
                steps_left = parking_lot_copy.find_solution(blocking_car.position - 2 + position_difference, dc(steps))
                if not steps_left and not steps_right:
                    return False
                elif steps_left and steps_right:
                    amount_steps_left = sum(steps_left.values(), -2 + position_difference)
                    amount_steps_right = sum(steps_right.values(), 1 + position_difference)
                    if abs(amount_steps_left) <= amount_steps_right:
                        steps = steps_left
                        steps[blocking_car.letter] = - 2 + position_difference
                    else:
                        steps = steps_right
                        steps[blocking_car.letter] = 1 + position_difference
                elif steps_left:
                    steps = steps_left
                    steps[blocking_car.letter] = -2 + position_difference
                else:
                    steps = steps_right
                    steps[blocking_car.letter] = 1 + position_difference
        if type(steps) == ChainMap:
            steps = dict(steps)
        return steps

    def visual(self, position: int = None) -> str:
        string = ""
        for index, normal_car in enumerate(self.normal_cars):
            if position is None and index == position:
                string += Fore.RED
                string += normal_car.letter
                string += Fore.RESET
            else:
                string += normal_car.letter
            string += " "
        string += "\n"
        for index in range(len(self.normal_cars)):
            if index in self.blocked_spots:
                if position is None and index == position:
                    string += Fore.RED
                    string += self.find_blocking_car(index).letter
                    string += Fore.RESET
                else:
                    string += self.find_blocking_car(index).letter
                string += " "
            else:
                string += "  "
        string += "\n"
        return string


class Car:
    def __init__(self, parent_lot: ParkingLot, letter: str, position: int) -> None:
        self.letter = letter
        self.parent_lot = parent_lot
        self._position = position

    @property
    def position(self) -> int:
        return self._position


class NormalCar(Car):
    def __init__(self, parent_lot: ParkingLot, letter: str) -> None:
        super().__init__(parent_lot, letter, get_index_of_letter(letter))

    @property
    def is_movable(self) -> bool:
        if self.position in self.parent_lot.blocked_spots:
            return False
        else:
            return True


class SideWaysCar(Car):
    def __init__(self, parent_lot: ParkingLot, letter: str, position: int) -> None:
        super().__init__(parent_lot, letter, position)
        self.parent_lot.update_blocked_spots(self)

    def is_movable(self, delta: int) -> bool:
        if delta > 0:
            delta += 1
        if self.position + delta in self.parent_lot.blocked_spots or self.position + delta \
                not in range(0, len(self.parent_lot.normal_cars)):
            return False
        else:
            return True

    @Car.position.setter
    def position(self, position: int) -> None:
        old_position = self._position
        self._position = position
        self.parent_lot.update_blocked_spots(self)


if __name__ == '__main__':
    parkplatz = ParkingLot(argv[1])
    print(parkplatz.visual())
    print(parkplatz)
