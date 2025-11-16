from collections.abc import Iterable
from typing import Protocol

from book_loader.elements import BookElement


class BookLoader(Protocol):
    def load(self) -> Iterable[BookElement]:
        raise NotImplementedError()
