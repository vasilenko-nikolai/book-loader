from collections.abc import Iterable
from typing import Protocol

from book_loader.elements import (
    BookElement,
    ChapterElement,
    ImageElement,
    ParagraphElement,
)


class BookFormatterVisitor(Protocol):
    def format(self, elements: Iterable[BookElement]) -> bytes:
        raise NotImplementedError()

    def visit_paragraph(self, paragraph: ParagraphElement) -> None:
        raise NotImplementedError()

    def visit_chapter(self, chapter: ChapterElement) -> None:
        raise NotImplementedError()

    def visit_image(self, image: ImageElement) -> None:
        raise NotImplementedError()
