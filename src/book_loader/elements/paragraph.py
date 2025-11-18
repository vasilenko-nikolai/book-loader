from typing import TYPE_CHECKING

from book_loader.elements._protocol import BookElement

if TYPE_CHECKING:
    from book_loader.formatters import BookFormatterVisitor


class ParagraphElement(BookElement):
    def __init__(
        self,
        text: str,
    ) -> None:
        self.text = text

    def accept(self, visitor: "BookFormatterVisitor") -> None:
        visitor.visit_paragraph(self)
