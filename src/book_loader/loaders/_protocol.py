from collections.abc import Iterable
from typing import Protocol

from book_loader.elements import BookElement
from book_loader.types.book import BookMeta


class BookLoader(Protocol):

    def fetch_content(self) -> Iterable[BookElement]:
        raise NotImplementedError()

    def fetch_meta(self) -> BookMeta:
        raise NotImplementedError()

