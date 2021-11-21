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

    def find_route(self) -> None:
        non_reducible = []
        self.hotels.sort()
        while len(self.hotels) > 4:
            min_hotel = None
            for hotel in self.hotels:
                if min_hotel is None or hotel not in non_reducible and hotel < min_hotel:
                    min_hotel = hotel
            if len(non_reducible) == len(self.hotels):
                break
            min_hotel_index = self.hotels.index(min_hotel)
            if min_hotel_index and min_hotel_index != len(self.hotels)-1:
                if self.hotels[min_hotel_index+1].distance - self.hotels[min_hotel_index-1].distance <= 360:
                    del self.hotels[min_hotel_index]
                    continue
            elif not min_hotel_index:
                if self.hotels[1].distance <= 360:
                    del self.hotels[min_hotel_index]
                    continue
            elif min_hotel_index == len(self.hotels)-1:
                if self.total_distance - self.hotels[-2].distance <= 360:
                    del self.hotels[min_hotel_index]
                    continue
            non_reducible.append(self.hotels[min_hotel_index])


if __name__ == '__main__':
    route = Route(argv[1])
    print(route.hotels)
