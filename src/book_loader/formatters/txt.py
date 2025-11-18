from collections.abc import Iterable

from book_loader.elements import BookElement
from book_loader.elements.chapter import ChapterElement
from book_loader.elements.paragraph import ParagraphElement
from book_loader.formatters._protocol import BookFormatterVisitor


class TxtFormatter(BookFormatterVisitor):
    def __init__(
        self,
    ) -> None:
        self._txt = ""

    def format(
        self,
        elements: Iterable[BookElement],
    ) -> bytes:
        for book_element in elements:
            book_element.accept(self)

        return self._txt.encode()

    def visit_chapter(
        self,
        chapter: ChapterElement,
    ) -> None:
        self._txt += "\n\n" + chapter.title + "\n\n"
        for element in chapter.elements:
            element.accept(self)

    def visit_paragraph(self, paragraph: ParagraphElement) -> None:
        self._txt += paragraph.text + "\n\n"
