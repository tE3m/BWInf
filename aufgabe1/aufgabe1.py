from sys import argv
from string import ascii_uppercase as letters


class Util:

    def get_index_of_letter(letter: str) -> int:
        return letters.index(letter)

    def get_letter_at_index(index: int) -> str:
        return letters[index]


class ParkingLot:

    def __init__(self) -> None:
        max_letter = file.readline()[2]
        for normal_car_letter in letters[:Util.get_index_of_letter(max_letter)]:
            self.normal_cars.append(NormalCar(self, normal_car_letter))
        for sideways_car in range(int(file.readline())):
            sideways_car_letter, position = file.readline().split()
            self.sideways_cars.append(SideWaysCar(self, sideways_car_letter, position))
        file.close()

    normal_cars = []
    sideways_cars = []


class Car:
    def __init__(self, parent_lot: ParkingLot, letter: str) -> None:
        self.letter = letter
        self.parent_lot = parent_lot

    letter: str


class NormalCar(Car):
    def __init__(self, parent_lot: ParkingLot, letter: str) -> None:
        super().__init__(parent_lot, letter)
        self.slot_number = Util.get_index_of_letter(self.letter)

    slot_number: int


class SideWaysCar(Car):
    def __init__(self, parent_lot: ParkingLot, letter: str, position: int) -> None:
        super().__init__(parent_lot, letter)
        self.position = position

    position: int


file = open(
    "/home/tarek/Projects/BWInf/Beispiele/a1-Schiebeparkplatz/beispieldaten/parkplatz0.txt",
    "r")  # TODO: Änderung zu argv[1]

parking_lot = ParkingLot()
