# Wird importiert, um die Datei mit Daten als Argument einlesen zu können
from sys import argv
# Wird importiert, um verschiedene Ausgabetypen für eine Methode annotieren zu können
from typing import Union


class Hotel:
    """Ein Hotel mit den Attributen `distance`, `rating` und dem zugehörigen `Route`-Objekt"""

    def __init__(self, distance: int, rating: float, parent_route):
        self.distance = distance
        self.rating = rating
        self.parent_route = parent_route
        self._daily_range = None

    def __repr__(self) -> str:
        return "Hotel({}, {})".format(self.distance, self.rating)

    def __str__(self) -> str:
        return "Position: {}, Bewertung: {}".format(self.distance, self.rating)

    def __lt__(self, other) -> bool:
        # Implementierung von __lt__ ermöglicht den "kleiner-als" Vergleich zwischen zwei Hotel-Objekten
        assert type(other) == Hotel
        return self.rating < other.rating

    @property
    def daily_range(self) -> list:
        """Stellt die Liste von Hotels dar, die innerhalb eines Tages erreicht werden können"""
        if not self._daily_range:
            self._daily_range = self.parent_route.range_per_day(self)
        return self._daily_range


class Route:

    def __init__(self, path: str) -> None:
        # Initialisierung aller Attribute
        self.min_rating = None
        self.hotels = []
        with open(path, "r") as file:
            hotel_amount = int(file.readline())
            self.total_distance = int(file.readline())
            for hotel in range(hotel_amount):
                distance, rating = file.readline().split(" ")
                self.hotels.append(Hotel(int(distance), float(rating), self))

    def __str__(self) -> str:
        # Formatiert die Lösung anschaulich
        possible_routes = self.find_route()
        if possible_routes:
            output = ""
            for index, hotel in enumerate(possible_routes):
                output += "{}. {}\n".format(index + 1, hotel)
        else:
            output = "Es wurde keine Lösung gefunden."
        return output

    def range_per_day(self, hotel: Hotel = None) -> filter:
        """Gibt für ein gegebenes Hotel `hotel` die verfügbaren Hotels zurück, die innerhalb eines Tages erreicht
        werden können

        :param hotel: das Hotel
        :return: die Liste von Hotels als `filter`-Objekt
        """
        if not hotel:
            start_distance = 0
        else:
            start_distance = hotel.distance
        return filter(lambda h: start_distance < h.distance <= start_distance + 360, self.hotels)

    def find_route(self, hotel: Hotel = None, counter: int = 0, stops: list[Hotel] = []) -> Union[bool, list[Hotel]]:
        """Findet rekursiv die optimale Route

        :param hotel: das Ausgangshotel
        :param counter: die Etappe der Route
        :param stops: die bisherigen Stopps
        :return: `False` falls keine Lösung vorhanden, sonst eine Liste von Hotels
        """
        stops = stops.copy()
        # Falls kein Hotel übergeben wird, befinden wir uns am Anfang der Route
        if hotel is None:
            daily_range = self.range_per_day()
        # sonst kann dieser Pfad in bestimmten Fällen bereits abgebrochen oder zurückgegeben werden
        else:
            # zB falls das eigene Rating niedriger ist als das niedrigste der aktuellen Lösung
            if self.min_rating and hotel.rating <= self.min_rating:
                return False
            daily_range = hotel.daily_range
            stops.append(hotel)
            # Haben wir innerhalb von 5 Tagen das Ziel erreicht, kann die Abfolge von Hotels zurückgegeben werden
            if counter <= 4 and self.total_distance - 360 <= hotel.distance:
                return stops
            # Ist es von diesem Hotel aus nicht mehr möglich, das Ziel innerhalb der Zeit zu erreichen,wird abgebrochen
            elif counter > 4 or counter <= 4 and self.total_distance - 360 * (5 - counter) > hotel.distance:
                return False
        solution = []
        # Jedes Hotel, das innerhalb eines Tages erreichbar ist, wird als nächster Schritt geprüft
        for stop in daily_range:
            possible_route = self.find_route(stop, counter + 1, stops)
            if possible_route:
                # Wird eine Lösung gefunden und es gibt bereits eine vorherige, überprüfe die beiden auf ihre minimale
                # Bewertung
                if solution:
                    solution = max(solution, possible_route.copy(), key=lambda r: min(r))
                    self.min_rating = min(solution).rating
                # Wird eine Lösung gefunden und es gibt bisher noch keine, setze sie als Lösung
                if not solution:
                    solution = possible_route.copy()
                    self.min_rating = min(solution).rating
        # Gib die Lösung aus, sofern es eine gibt
        if solution:
            return solution
        else:
            return False


if __name__ == '__main__':
    route = Route(argv[1])
    print(route)
