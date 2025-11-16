from collections.abc import Iterable
from typing import Protocol

from book_loader.elements import BookElement


class BookFormater(Protocol):
    def format(self, elements: Iterable[BookElement]) -> bytes:
        raise NotImplementedError()
