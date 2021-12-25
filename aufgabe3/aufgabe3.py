NUMBERS = {
    0: [True, True, True, False, True, True, True],
    1: [False, False, True, False, False, True, False],
    2: [True, False, True, True, True, False, True],
    3: [True, False, True, True, False, True, True],
    4: [False, True, True, True, False, True, False],
    5: [True, True, False, True, False, True, True],
    6: [True, True, False, True, True, True, True],
    7: [True, False, True, False, False, True, False],
    8: [True, True, True, True, True, True, True],
    9: [True, True, True, True, False, True, True],
    10: [True, True, True, True, True, True, False],
    11: [False, True, False, True, True, True, True],
    12: [True, True, False, False, True, False, True],
    13: [False, False, True, True, True, True, True],
    14: [True, True, False, True, True, False, True],
    15: [True, True, False, True, True, False, False]
}


class HexDigit:
    """Eine Hexadezimalziffer"""
    value: int
    representation: list[bool]

    def __init__(self, value: str) -> None:
        # Speichere die Dezimalrepräsentation der gegebenen Ziffer als Attribut
        self.value = int(value, 16)
        self.representation = NUMBERS[self.value]

    def __repr__(self) -> str:
        return "HexDigit({})".format(self.value)

    def move_distance(self, other: int) -> int:
        amount = len(self.differing_segments(other))
        return amount // 2 + amount % 2

    def segment_difference(self, other: int) -> int:
        return len(list(filter(lambda x: x, self.representation))) - len(list(filter(lambda x: x, NUMBERS[other])))

    def differing_segments(self, other: int):
        return [index for index in range(7) if self.representation[index] != NUMBERS[other][index]]

    def digit_with_distance(self, distance: int, moves: int):
        for new_digit in range(0, 16):
            if self.segment_difference(new_digit) == distance and self.move_distance(new_digit) <= moves:
                return moves - self.move_distance(new_digit), new_digit


class HexNumber:
    """Eine Hexadezimalzahl"""
    digits: list[HexDigit]
    moves: int

    def __init__(self, number: str, moves: int):
        # Wandle den gegebenen Hexadezimal-String zu einer Liste aus Hexadezimalziffern um
        self.digits = [HexDigit(digit) for digit in number]
        self.moves = moves

    def __repr__(self) -> str:
        return str([repr(digit) for digit in self.digits])

    def __str__(self) -> str:
        buffer = ""
        lines = ["#######", "##   ##", "#######", "##   ##", "#######"]
        index = 0
        for line in lines:
            for digit in self.digits:
                segments = line.split("   ")
                for offset, segment in enumerate(segments):
                    segment = segment if digit.representation[index + offset] else "".join(" " for _ in segment)
                    if line == "#######":
                        if segment[:2] == "  " and (index == 0 or index == 3):
                            segment = "##" + segment[2:] if digit.representation[index + 1] else segment
                            segment = segment[:-2] + "##" if digit.representation[index + 2] else segment
                        if segment[-2:] == "  " and (index == 3 or index == 6):
                            segment = segment[:-2] + "##" if digit.representation[index - 1] else segment
                            segment = "##" + segment[2:] if digit.representation[index - 2] else segment
                    buffer += segment + "   "
            buffer += "\n"
            index += len(segments)
        return buffer

    def highest_within_moves(self) -> None:
        for index, digit in enumerate(self.digits):
            if digit.value == 15:
                continue
            for higher_digit in range(15, digit.value, -1):
                if digit.move_distance(higher_digit) <= self.moves:
                    if digit.segment_difference(higher_digit) == 0:
                        self.moves -= digit.move_distance(higher_digit)
                        to_be_removed = {index: [segment for segment in digit.differing_segments(higher_digit) if
                                                 digit.representation[segment]]}
                    else:
                        old_moves = self.moves
                        self.moves -= digit.move_distance(higher_digit)
                        to_be_removed = self.additional_segments(index, digit.segment_difference(higher_digit))
                        if to_be_removed is None:
                            self.moves = old_moves
                            continue
                    to_be_added = (segment for segment in digit.differing_segments(higher_digit) if
                                   NUMBERS[higher_digit][segment])
                    for other_digit, moves in to_be_removed.items():
                        for segment in moves:
                            self.digits[other_digit].representation[segment] = False
                            digit.representation[next(to_be_added)] = True
                            print(self)
            if self.moves == 0:
                break

    def additional_segments(self, start_index: int, missing: int):
        segments = {}
        for index, digit in enumerate(reversed(self.digits[start_index:])):
            for amount in range(missing, 0, -1):
                moves_and_digit = digit.digit_with_distance(amount, self.moves)
                if moves_and_digit is not None:
                    self.moves, new_digit = moves_and_digit
                    missing -= amount
                    segments[index] = [segment for segment in digit.differing_segments(new_digit) if
                                       digit.representation[segment]]
            if not missing:
                return segments


if __name__ == '__main__':
    hexnumber = HexNumber("d24", 3)
    print(hexnumber)
    hexnumber.highest_within_moves()
