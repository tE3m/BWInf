from datetime import datetime
from time import sleep
from random import randint
from sys import argv
from itertools import chain
from typing import TypedDict


class PixelValues(TypedDict):
    color: int
    x: int
    y: int


class SproutValues(PixelValues):
    creation_time: int
    up: int
    down: int
    right: int
    left: int


class Pixel:
    color: int
    x: int
    y: int

    def __init__(self, values: PixelValues):
        self.color, self.x, self.y = values.values()

    def __repr__(self):
        return "Pixel({}, {}, {})".format(self.color, self.x, self.y)

    def __str__(self):
        return "Pixel({}, {}) = {}".format(self.x, self.y, self.color)


class Sprout(Pixel):
    creation_time: int
    up: int
    down: int
    right: int
    left: int

    def __init__(self, values: SproutValues):
        super().__init__({k: v for k, v in values.items() if k == "color" or k == "x" or k == "y"})
        self.color, self.creation_time, self.x, self.y, self.up, self.down, self.right, self.left = values.values()

    def __repr__(self):
        return "Sprout({}, {})".format(self.x, self.y)


class Picture:
    pixels: list[list[Sprout]]
    sprouts: list[Sprout]
    filename: str
    active_edges: list[Sprout]

    def __init__(self, sprouts: list[SproutValues]):
        for sprout in sprouts:
            self.sprouts.append(Sprout(sprout))
        self.filename = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

    def simulate(self, update=False):
        while not all(chain.from_iterable(self.pixels)):
            if update:
                self.draw()
                sleep(1)
            # TODO: Simulation implementieren



    def draw(self):
        with open(self.filename, "wx") as file:
            for row in self.pixels:
                for pixel in row:
                    file.write(str(pixel.color if pixel else 0))


if __name__ == '__main__':
    values: PixelValues = {"color": randint(1, 255), "x": randint(0, 1919), "y": randint(0, 1079)}
    pixel = Pixel(values)
    print(pixel)
