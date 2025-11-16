from collections.abc import Iterable

from book_loader.elements import BookElement
from book_loader.formatters._protocol import BookFormater
from book_loader.visitors import TxtVisitor


class TxtFormatter(BookFormater):
    def __init__(
        self,
    ) -> None:
        self._visitor = TxtVisitor()

    def format(
        self,
        elements: Iterable[BookElement],
    ) -> bytes:
        for book_element in elements:
            book_element.accept(self._visitor)

        return self._visitor.txt.encode()
