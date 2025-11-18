from collections.abc import Iterable

from book_loader.elements._protocol import BookElement
from book_loader.elements.chapter import ChapterElement
from book_loader.elements.paragraph import ParagraphElement
from book_loader.formatters._protocol import BookFormatterVisitor


class Fb2Formatter(BookFormatterVisitor):
    def __init__(self) -> None:
        self._xml = ""

    def format(
        self,
        elements: Iterable[BookElement],
    ) -> bytes:
        self._add_header()

        for element in elements:
            element.accept(self)

        self._add_footer()
        return self._xml.encode()

    def _add_header(self) -> None:
        self._xml += """
        <?xml version="1.0" encoding="utf-8"?>
        <FictionBook xmlns="http://www.gribuser.ru/xml/fictionbook/2.0" xmlns:l="http://www.w3.org/1999/xlink">
            <description>
            </description>
        <body>
        """

    def _add_footer(self) -> None:
        self._xml += "</body>"
        self._xml += "</FictionBook>"

    def visit_chapter(self, chapter: ChapterElement) -> None:
        self._xml += "<section>"

        self._xml += f"<title><p>{chapter.title}</p></title>"
        for element in chapter.elements:
            element.accept(self)

        self._xml += "</section>"

    def visit_paragraph(self, paragraph: ParagraphElement) -> None:
        self._xml += "<p>" + paragraph.text + "</p>"
