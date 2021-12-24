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


class HexNumber:
    """Eine Hexadezimalzahl"""
    digits: list[HexDigit]

    def __init__(self, number: str):
        # Wandle den gegebenen Hexadezimal-String zu einer Liste aus Hexadezimalziffern um
        self.digits = [HexDigit(digit) for digit in number]

    def __repr__(self) -> str:
        return str([repr(digit) for digit in self.digits])

    def __str__(self) -> str:
        buffer = ""
        lines = ["#######", "##   ##", "#######", "##   ##", "#######"]
        index = 0
        for line in lines:
            for digit in self.digits:
                for offset, segment in enumerate(line.split("   ")):
                    segment = segment if digit.representation[index+offset] else "".join(" " for _ in segment)
                    if line == "#######":
                        if segment[:2] == "  " and (index == 0 or index == 3):
                            segment = "##" + segment[2:] if digit.representation[index+1] else segment
                            segment = segment[:-2] + "##" if digit.representation[index+2] else segment
                        if segment[-2:] == "  " and (index == 3 or index == 6):
                            segment = segment[:-2] + "##" if digit.representation[index-1] else segment
                            segment = "##" + segment[2:] if digit.representation[index-2] else segment
                    buffer += segment + "   "
            buffer += "\n"
            index += len(line.split("   "))
        return buffer
