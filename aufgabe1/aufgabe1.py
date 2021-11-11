from sys import argv
from string import ascii_uppercase as letters


class Util:

    def get_index_of_letter(letter: str) -> int:
        return letters.index(letter)

    def get_letter_at_index(index: int) -> str:
        return letters[index]


class ParkingLot:

    def __init__(self) -> None:
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
        self._blocked_spots[car] = [car.position, car.position+1]


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
        self._position = position
        self.parent_lot.update_blocked_spots(self)


file = open(
    "/home/tarek/Projects/BWInf/Beispiele/a1-Schiebeparkplatz/beispieldaten/parkplatz0.txt",
    "r")  # TODO: Änderung zu argv[1]

parking_lot = ParkingLot()
