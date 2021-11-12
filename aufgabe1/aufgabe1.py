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

    @property
    def blocked_spots(self) -> list:
        return sum(list(self._blocked_spots.values()), [])

    def update_blocked_spots(self, car) -> None:
        if car.position in self.blocked_spots and self.find_blocking_car(car.position) != car or car.position + 1 in self.blocked_spots and self.find_blocking_car(car.position+1) != car:
            raise SpaceTakenError("Dieser Platz ist bereits belegt.")
        self._blocked_spots[car] = [car.position, car.position + 1]

    @property
    def solution(self) -> dict:
        solution_dict = {}
        for normal_car in self.normal_cars:
            solution_dict[normal_car.letter] = self.find_solution(normal_car.position, [])
            pass
        return solution_dict

    def find_solution(self, position: int, steps=[]) -> list:
        if position in self.blocked_spots:
            sideways_cars_copy = deepcopy(self._sideways_cars)
            blocked_spots_copy = deepcopy(self._blocked_spots)
            blocking_car = self.find_blocking_car(position)
            position_difference = position - blocking_car.position
            try:
                disposition = min(abs(-2+position_difference), 1+position_difference)
                if disposition == abs(-2+position_difference):
                    disposition *= -1
                blocking_car.position += disposition
                steps.append({blocking_car.letter: disposition})
            except ValueError:
                try:
                    disposition = max(abs(-2 + position_difference), 1 + position_difference)
                    if disposition == abs(-2 + position_difference):
                        disposition *= -1
                    blocking_car.position += disposition
                    steps.append({blocking_car.letter: disposition})
                except ValueError:
                    steps_right = self.find_solution(blocking_car.position+2, steps)
                    steps_left = self.find_solution(blocking_car.position-1, steps)
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


class Car:
    def __init__(self, parent_lot: ParkingLot, letter: str, position: int) -> None:
        self.letter = letter
        self.parent_lot = parent_lot
        self._position = position

    @property
    def position(self) -> int:
        return self._position

    @property
    def is_movable(self) -> bool:
        pass


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

    def is_movable(self, delta: int):
        if delta > 0:
            delta += 1
        if self.position + delta in self.parent_lot.blocked_spots:
            return False
        else:
            return True

    @Car.position.setter
    def position(self, position: int) -> None:
        if position >= len(self.parent_lot.normal_cars) - 1 or position < 0:
            raise NonExistentSpaceError("Diesen Platz gibt es nicht.")
        old_position = self._position
        try:
            self._position = position
            self.parent_lot.update_blocked_spots(self)
        except SpaceTakenError:
            self._position = old_position
