from book_loader.elements.chapter import ChapterElement
from book_loader.elements.paragraph import ParagraphElement
from book_loader.visitors._protocol import BookElementVisitor


class TxtVisitor(BookElementVisitor):
    def __init__(self) -> None:
        self._txt = ""

    def visit_chapter(
        self,
        chapter: ChapterElement,
    ) -> None:
        self._txt += "\n\n" + chapter.title + "\n\n"
        for element in chapter.elements:
            element.accept(self)

    def visit_paragraph(self, paragraph: ParagraphElement) -> None:
        self._txt += paragraph.text + "\n\n"

    @property
    def txt(self) -> str:
        return self._txt
