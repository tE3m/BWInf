from sys import argv
from string import ascii_uppercase as letters
from copy import deepcopy


class SpaceTakenError(ValueError):
    pass


class NonExistentSpaceError(ValueError):
    pass


class Util:

    @staticmethod
    def get_index_of_letter(letter: str) -> int:
        return letters.index(letter)

    @staticmethod
    def get_letter_at_index(index: int) -> str:
        return letters[index]


class ParkingLot:

    def __init__(self, file_path: str) -> None:
        file = open(file_path, "r")
        self.normal_cars = []
        self._sideways_cars = []
        self._blocked_spots = {}
        max_letter = file.readline()[2]
        for normal_car_letter in letters[:Util.get_index_of_letter(max_letter) + 1]:
            self.normal_cars.append(NormalCar(self, normal_car_letter))
        for sideways_car in range(int(file.readline())):
            sideways_car_letter, position = file.readline().split()
            self._sideways_cars.append(SideWaysCar(self, sideways_car_letter, int(position)))
        file.close()

    def __str__(self) -> str:
        solution = self.solution
        output = ""
        for slot in solution:
            if solution[slot] == [-1]:
                output += slot + ": nicht lösbar\n"
            else:
                output += slot + ": "
                for element in solution[slot]:
                    (blocking_car, move) = next(iter(element.items()))
                    if move > 0:
                        direction = "rechts"
                    else:
                        direction = "links"
                    output += blocking_car + " " + str(abs(move)) + " " + direction
                    if element != solution[slot][-1]:
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
            raise SpaceTakenError("Dieser Platz ist bereits belegt.")
        else:
            self._blocked_spots[car] = [car.position, car.position + 1]
        pass

    @property
    def solution(self) -> dict:
        solution_dict = {}
        for normal_car in self.normal_cars:
            solution_dict[normal_car.letter] = self.find_solution(normal_car.position, [])
        return solution_dict

    def find_solution(self, position: int, steps=None) -> list:
        if steps is None:
            steps = []
        if position not in range(len(self.normal_cars)):
            steps = [-1]
        elif position in self.blocked_spots:
            sideways_cars_copy = deepcopy(self._sideways_cars)
            blocked_spots_copy = deepcopy(self._blocked_spots)
            blocking_car = self.find_blocking_car(position)
            position_difference = position - blocking_car.position
            if blocking_car.is_movable(0):
                disposition = min(abs(-2 + position_difference), 1 + position_difference)
                if disposition == abs(-2 + position_difference):
                    disposition *= -1
                if blocking_car.is_movable(disposition):
                    blocking_car.position += disposition
                    steps.append({blocking_car.letter: disposition})
                else:
                    disposition = max(abs(-2 + position_difference), 1 + position_difference)
                    if disposition == abs(-2 + position_difference):
                        disposition *= -1
                    if blocking_car.is_movable(disposition):
                        blocking_car.position += disposition
                        steps.append({blocking_car.letter: disposition})
                    else:
                        steps = [-1]
            else:
                steps_right = self.find_solution(blocking_car.position + 2, steps)
                steps_left = self.find_solution(blocking_car.position - 1, steps)
                if steps_left == [-1] and steps_right == [-1]:
                    steps = [-1]
                elif steps_left != [-1] and steps_right != [-1]:
                    if steps_left <= steps_right:
                        steps = steps_left
                        steps.append({blocking_car.letter: -1})
                    else:
                        steps = steps_right
                        steps.append({blocking_car.letter: 1})
                elif steps_left != [-1]:
                    steps = steps_left
                    steps.append({blocking_car.letter: -1})
                else:
                    steps = steps_right
                    steps.append({blocking_car.letter: 1})
            self._sideways_cars = sideways_cars_copy
            self._blocked_spots = blocked_spots_copy
        return steps

    def find_blocking_car(self, position: int):
        return self._sideways_cars[int(self.blocked_spots.index(position) / 2)]

    def visual(self) -> None:
        for normal_car in self.normal_cars:
            print(normal_car.letter, end=" ")
        print()
        for position in range(len(self.normal_cars)):
            if position in self.blocked_spots:
                print(self.find_blocking_car(position).letter, end=" ")
            else:
                print(" ", end=" ")
        print()


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
        super().__init__(parent_lot, letter, Util.get_index_of_letter(letter))

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
        if delta == 0:
            return self.is_movable(-1) or self.is_movable(1)
        if delta > 0:
            delta += 1
        if self.position + delta in self.parent_lot.blocked_spots or self.position + delta not in range(0, len(self.parent_lot.normal_cars)):
            return False
        else:
            return True

    @Car.position.setter
    def position(self, position: int) -> None:
        old_position = self._position
        self._position = position
        try:
            self.parent_lot.update_blocked_spots(self)
        except SpaceTakenError or NonExistentSpaceError as error:
            self._position = old_position
            raise error
