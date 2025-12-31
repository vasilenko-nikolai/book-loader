import base64
from collections.abc import Iterable

from book_loader.elements._protocol import BookElement
from book_loader.elements.chapter import ChapterElement
from book_loader.elements.image import ImageElement
from book_loader.elements.paragraph import ParagraphElement
from book_loader.formatters._protocol import BookFormatterVisitor
from book_loader.types import BookMeta


class Fb2Formatter(BookFormatterVisitor):
    def __init__(self, book_meta: BookMeta | None = None) -> None:
        self._xml = ""
        if book_meta is None:
            book_meta = BookMeta()

        self._book_meta = book_meta
        self._binaries: list[str] = []

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
        self._xml += f"""
        <?xml version="1.0" encoding="utf-8"?>
        <FictionBook xmlns="http://www.gribuser.ru/xml/fictionbook/2.0" xmlns:l="http://www.w3.org/1999/xlink">
            <description>
                <title-info>
                    {self._xml_genres}
                </title-info>
                {self._xml_book_title}
                {self._xml_authors}
                {self._xml_annotation}
            </description>
        <body>
        """

    @property
    def _xml_genres(self) -> str:
        if self._book_meta.genres is None:
            return ""

        return "\n".join(f"<genre>{genre}</genre>" for genre in self._book_meta.genres)

    @property
    def _xml_book_title(self) -> str:
        if self._book_meta.name is None:
            return ""

        return f"<book-title>{self._book_meta.name}</book-title>"

    @property
    def _xml_authors(self) -> str:
        if self._book_meta.authors is None:
            return ""

        return "\n".join(
            f"""
            <author>
                <nickname>{author}</nickname>
            </author>
            """
            for author in self._book_meta.authors
        )

    @property
    def _xml_annotation(self) -> str:
        if self._book_meta.description is None:
            return ""

        return "<annotation>" + self._book_meta.description + "</annotation>"

    def _add_footer(self) -> None:
        self._xml += "</body>"
        self._xml += "\n".join(self._binaries)
        self._xml += "</FictionBook>"

    def visit_chapter(self, chapter: ChapterElement) -> None:
        self._xml += "<section>"

        self._xml += f"<title><p>{chapter.title}</p></title>"
        for element in chapter.elements:
            element.accept(self)

        self._xml += "</section>"

    def visit_paragraph(self, paragraph: ParagraphElement) -> None:
        self._xml += "<p>" + paragraph.text + "</p>"

    def visit_image(self, image: ImageElement) -> None:
        image64 = base64.b64encode(image.image)
        image_id = f"image{len(self._binaries)}"
        self._binaries.append(
            f"""
            <binary id="{image_id}" content-type="image/jpeg">
            {image64.decode()}
            </binary>
            """
        )
        self._xml += f'<image l:href="#{image_id}" />'
