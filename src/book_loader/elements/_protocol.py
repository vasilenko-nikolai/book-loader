from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from book_loader.formatters import BookFormatterVisitor


class BookElement(Protocol):
    def accept(self, visitor: "BookFormatterVisitor") -> None:
        raise NotADirectoryError()
