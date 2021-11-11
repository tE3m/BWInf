from sys import argv
from string import ascii_uppercase as letters


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
        for normal_car_letter in letters[:Util.get_index_of_letter(max_letter)+1]:
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


class Car:
    def __init__(self, parent_lot: ParkingLot, letter: str) -> None:
        self.letter = letter
        self.parent_lot = parent_lot


class NormalCar(Car):
    def __init__(self, parent_lot: ParkingLot, letter: str) -> None:
        super().__init__(parent_lot, letter)
        self.slot_number = Util.get_index_of_letter(self.letter)


class SideWaysCar(Car):
    def __init__(self, parent_lot: ParkingLot, letter: str, position: int) -> None:
        super().__init__(parent_lot, letter)
        self._position = position
        self.parent_lot.update_blocked_spots(self)

    @property
    def position(self) -> int:
        return self._position

    @position.setter
    def position(self, position: int) -> None:
        if position >= len(self.parent_lot.normal_cars)-1 or position < 0:
            raise NonExistentSpaceError("Diesen Platz gibt es nicht.")
        old_position = self._position
        try:
            self._position = position
            self.parent_lot.update_blocked_spots(self)
        except SpaceTakenError:
            self._position = old_position
