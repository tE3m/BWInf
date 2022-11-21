from re import Pattern, compile, findall, IGNORECASE, MULTILINE
from sys import argv


class Book:
    book_text: str
    _pattern: Pattern

    def __init__(self, book_text: str) -> None:
        self.book_text = book_text

    def find_passage(self) -> list[str]:
        matches = findall(self.pattern, self.book_text)
        return matches

    @property
    def pattern(self) -> Pattern:
        return self._pattern

    @pattern.setter
    def pattern(self, new_pattern: str):
        self._pattern = compile(new_pattern.replace("_", r"\w+"), IGNORECASE | MULTILINE)


if __name__ == '__main__':
    with open(argv[1], "r") as text:
        book = Book(" ".join(text.readlines()))
    with open(argv[2], "r") as task:
        book.pattern = task.readline().strip()
    print("Die passenden Stellen sind:\n")
    for index, match in enumerate(book.find_passage()):
        print(str(index+1) + ".", match)
