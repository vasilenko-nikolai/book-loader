from collections.abc import Iterable
from typing import TYPE_CHECKING

from book_loader.elements._protocol import BookElement

if TYPE_CHECKING:
    from book_loader.visitors import BookElementVisitor


class ChapterElement(BookElement):
    def __init__(
        self,
        title: str,
        elements: Iterable[BookElement],
    ) -> None:
        self.title = title
        self.elements = elements

    def accept(
        self,
        visitor: "BookElementVisitor",
    ) -> None:
        visitor.visit_chapter(self)
