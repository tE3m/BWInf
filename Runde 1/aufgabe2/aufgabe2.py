from math import floor, sin
from datetime import datetime
from random import randint
from sys import argv
from itertools import chain
from typing import TypedDict


class PixelValues(TypedDict):
    color: int
    x: int
    y: int


class SproutValues(PixelValues):
    draw_at: int
    up: int
    down: int
    right: int
    left: int


class Pixel:
    """
    Ein Pixel
    """
    color: int
    x: int
    y: int

    def __init__(self, values: PixelValues) -> None:
        self.color, self.x, self.y = values.values()

    def __repr__(self) -> str:
        return "Pixel({}, {}, {})".format(self.color, self.x, self.y)

    def __str__(self) -> str:
        return "Pixel({}, {}) = {}".format(self.x, self.y, self.color)


class Sprout(Pixel):
    """
    Ein Kristallisationskeim
    """
    draw_at: int
    up: int
    down: int
    right: int
    left: int

    def __init__(self, values: SproutValues) -> None:
        super().__init__({k: v for k, v in values.items() if k == "color" or k == "x" or k == "y"})
        self.color, self.x, self.y, self.draw_at, self.up, self.down, self.right, self.left = values.values()

    def __repr__(self) -> str:
        return "Sprout({}, {})".format(self.x, self.y)


class Spread(Pixel):
    """
    Ein Auswuchs des Kristalls
    """
    draw_at: int
    parent_sprout: Sprout

    def __init__(self, values: PixelValues, draw_at: int, parent_sprout: Sprout) -> None:
        super().__init__(values)
        self.draw_at = draw_at
        self.parent_sprout = parent_sprout


class Picture:
    """
    Das Bild
    """
    width: int
    height: int
    pixels: list[list[int | None]]
    sprouts: list[Sprout]
    filename: str
    active_edges: filter

    def __init__(self, width: int, height: int, sprouts: list[Sprout]) -> None:
        self.width = width
        self.height = height
        self.pixels = [[None for _ in range(width)] for _ in range(self.height)]
        self.sprouts = sprouts
        self.filename = datetime.now().strftime("Kristall_%d-%m-%Y_%H-%M-%S")

    def simulate(self, update=False) -> None:
        """
        Simuliert das Wachstum der Keime

        :param update: bei `True` wird das Bild nach jedem Simulationsschritt in die Datei geschrieben.
        """
        future_sprouts = self.sprouts.copy()
        step = 0
        while not all(chain.from_iterable(self.pixels)):
            if update:
                self.draw()
                # erlaubt das Setzen eines Breakpoints des Debuggers, um nach jedem Draw anzuhalten
                pass
            # sortiert bereits gezeichnete Pixel aus
            future_sprouts = [sprout for sprout in future_sprouts if sprout.draw_at >= step]
            # filtert nach den Pixeln, die in diesem Schritt gezeichnet werden
            self.active_edges = filter(lambda s: s.draw_at == step, future_sprouts)
            for sprout in self.active_edges:
                # falls der betroffene Pixel bereits einen Wert hat, wird dieser nicht überschrieben
                if self.pixels[sprout.y][sprout.x] is not None:
                    continue
                self.pixels[sprout.y][sprout.x] = sprout.color
                # bereitet die nächste Ausbreitungsstufe vor
                if sprout.y != 0 and self.pixels[sprout.y - 1][sprout.x] is None:
                    if type(sprout) == Sprout:
                        up = Spread({"color": sprout.color, "x": sprout.x, "y": sprout.y - 1}, step + sprout.up,
                                    parent_sprout=sprout)
                    else:
                        up = Spread({"color": sprout.color, "x": sprout.x, "y": sprout.y - 1},
                                    step + sprout.parent_sprout.up, parent_sprout=sprout.parent_sprout)
                    future_sprouts.append(up)
                if sprout.y < self.height - 1 and self.pixels[sprout.y + 1][sprout.x] is None:
                    if type(sprout) == Sprout:
                        down = Spread({"color": sprout.color, "x": sprout.x, "y": sprout.y + 1}, step + sprout.down,
                                      parent_sprout=sprout)
                    else:
                        down = Spread({"color": sprout.color, "x": sprout.x, "y": sprout.y + 1},
                                      step + sprout.parent_sprout.down, parent_sprout=sprout.parent_sprout)
                    future_sprouts.append(down)
                if sprout.x < self.width - 1 and self.pixels[sprout.y][sprout.x + 1] is None:
                    if type(sprout) == Sprout:
                        right = Spread({"color": sprout.color, "x": sprout.x + 1, "y": sprout.y}, step + sprout.right,
                                       parent_sprout=sprout)
                    else:
                        right = Spread({"color": sprout.color, "x": sprout.x + 1, "y": sprout.y},
                                       step + sprout.parent_sprout.right, parent_sprout=sprout.parent_sprout)
                    future_sprouts.append(right)
                if sprout.x != 0 and self.pixels[sprout.y][sprout.x - 1] is None:
                    if type(sprout) == Sprout:
                        left = Spread({"color": sprout.color, "x": sprout.x - 1, "y": sprout.y}, step + sprout.left,
                                      parent_sprout=sprout)
                    else:
                        left = Spread({"color": sprout.color, "x": sprout.x - 1, "y": sprout.y},
                                      step + sprout.parent_sprout.left, parent_sprout=sprout.parent_sprout)
                    future_sprouts.append(left)
            step += 1
        self.draw()

    def draw(self) -> None:
        """
        Schreibt das Bild in die Datei
        """
        with open(self.filename, "w") as file:
            file.write("P2 {} {} 65535\n".format(self.width, self.height))
            for row in self.pixels:
                for pixel in row:
                    file.write(str(pixel if pixel is not None else 0) + " ")
                file.write("\n")


def sprout_randomizer(width: int, height: int, amount: int, min_velocity: int) -> list[Sprout]:
    """
    Gibt eine Liste pseudozufälliger Kristallisationskeime zurück

    :param height: die Höhe des Bildes
    :param width: die Breite des Bildes
    :param amount: die Anzahl zu generierender Keime
    :param min_velocity: die geringste erlaubte Ausbreitungsgeschwindigkeit
    :return: eine Liste mit Kristallisationskeimen
    """
    values: list[SproutValues] = [{"color": 0,
                                   "x": randint(0, width - 1),
                                   "y": randint(0, height - 1),
                                   "draw_at": randint(0, 15),
                                   "up": randint(1, min_velocity),
                                   "down": randint(1, min_velocity),
                                   "right": randint(1, min_velocity),
                                   "left": randint(1, min_velocity)
                                   } for _ in range(amount)]
    for value in values:
        # berechnet einen Grauwert in Abhängigkeit der Richtung
        value["color"] = floor(sin(
            (value["up"] + value["down"] + value["right"] + value["left"]) / (min_velocity * 4)) * 65535)
    return [Sprout(value) for value in values]


if __name__ == '__main__':
    w, h, amt, vel = map(int, argv[1:])
    picture = Picture(w, h, sprout_randomizer(w, h, amt, vel))
    picture.simulate()
