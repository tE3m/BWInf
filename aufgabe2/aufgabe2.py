from sys import argv
from collections import ChainMap


class Hotel:

    def __init__(self, distance: int, rating: float):
        self.distance = distance
        self.rating = rating

    def __repr__(self) -> str:
        return "Hotel({}, {})".format(self.distance, self.rating)

    def __str__(self) -> str:
        return "Position: {}, Bewertung: {}".format(self.distance, self.rating)


class Route:

    def __init__(self, path: str) -> None:
        self.hotels = []
        self.position = 0
        with open(path, "r") as file:
            hotel_amount = int(file.readline())
            self.total_distance = int(file.readline())
            for hotel in range(hotel_amount):
                distance, rating = file.readline().split(" ")
                self.hotels.append(Hotel(int(distance), float(rating)))

    def __str__(self) -> str:
        output = ""
        for index, hotel in enumerate(self.find_route()):
            output += "{}. {}\n".format(index + 1, hotel)
        return output

    def range_per_day(self) -> list[Hotel]:
        return [hotel for hotel in self.hotels if self.position < hotel.distance < self.position + 360]

    def find_route(self) -> list[Hotel]:
        chosen_hotels = []
        while self.position < self.total_distance - 360:
            chosen_hotels.append(max(self.range_per_day(), key=lambda h: h.rating))
            self.position = chosen_hotels[-1].distance
        return chosen_hotels


if __name__ == '__main__':
    route = Route(argv[1])
    print(route.hotels)
