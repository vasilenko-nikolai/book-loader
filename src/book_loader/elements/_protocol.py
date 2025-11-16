from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from book_loader.visitors import BookElementVisitor


class BookElement(Protocol):
    def accept(self, visitor: "BookElementVisitor") -> None:
        raise NotADirectoryError()
