from typing import Protocol

from book_loader.elements import ChapterElement, ParagraphElement


class BookElementVisitor(Protocol):
    def visit_paragraph(self, paragraph: ParagraphElement) -> None:
        raise NotImplementedError()

    def visit_chapter(self, chapter: ChapterElement) -> None:
        raise NotImplementedError()
