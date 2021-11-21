from sys import argv
from typing import Union


class Hotel:

    def __init__(self, distance: int, rating: float, parent_route):
        self.distance = distance
        self.rating = rating
        self.parent_route = parent_route

    def __repr__(self) -> str:
        return "Hotel({}, {})".format(self.distance, self.rating)

    def __str__(self) -> str:
        return "Position: {}, Bewertung: {}".format(self.distance, self.rating)

    def __lt__(self, other):
        assert type(other) == Hotel
        return self.rating < other.rating

    @property
    def daily_range(self):
        return self.parent_route.range_per_day(self)


class Route:

    def __init__(self, path: str) -> None:
        self.min_rating = None
        self.hotels = []
        with open(path, "r") as file:
            hotel_amount = int(file.readline())
            self.total_distance = int(file.readline())
            for hotel in range(hotel_amount):
                distance, rating = file.readline().split(" ")
                self.hotels.append(Hotel(int(distance), float(rating), self))

    def __str__(self) -> str:
        possible_routes = self.find_route()
        if possible_routes:
            output = ""
            for index, hotel in enumerate(possible_routes):
                output += "{}. {}\n".format(index + 1, hotel)
        else:
            output = "Es wurde keine Lösung gefunden."
        return output

    def range_per_day(self, hotel: Hotel = None) -> list[Hotel]:
        if not hotel:
            start_distance = 0
        else:
            start_distance = hotel.distance
        return filter(lambda h: start_distance < h.distance <= start_distance + 360, self.hotels)

    def find_route(self, hotel: Hotel = None, counter: int = 0, stops: list[Hotel] = []) -> Union[bool, list[Hotel]]:
        stops = stops.copy()
        if hotel is None:
            daily_range = self.range_per_day()
        else:
            if self.min_rating and hotel.rating <= self.min_rating:
                return False
            daily_range = hotel.daily_range
            stops.append(hotel)
            if counter <= 4 and self.total_distance - 360 <= hotel.distance:
                return stops
            elif counter <= 4 and self.total_distance - 360 * (5 - counter) > hotel.distance:
                return False
        if counter < 4:
            solution = []
            for stop in daily_range:
                possible_route = self.find_route(stop, counter + 1, stops)
                if possible_route and solution:
                    solution = max(solution, possible_route.copy(), key=lambda r: min(r))
                    self.min_rating = min(solution).rating
                elif possible_route and not solution:
                    solution = possible_route.copy()
                    self.min_rating = min(solution).rating
            if solution:
                return solution
            else:
                return False
        else:
            return False


if __name__ == '__main__':
    route = Route(argv[1])
    print(route)
