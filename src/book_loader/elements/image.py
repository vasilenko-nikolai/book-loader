from typing import TYPE_CHECKING

from book_loader.elements._protocol import BookElement

if TYPE_CHECKING:
    from book_loader.formatters import BookFormatterVisitor


class ImageElement(BookElement):
    def __init__(self, image: bytes) -> None:
        self.image = image

    def accept(
        self,
        visitor: "BookFormatterVisitor",
    ) -> None:
        visitor.visit_image(self)
