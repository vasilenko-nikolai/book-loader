import logging
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any, ClassVar

import requests
from requests.sessions import HTTPAdapter
from urllib3.util.retry import Retry

from book_loader.elements import BookElement, ChapterElement, ParagraphElement
from book_loader.loaders._protocol import BookLoader
from book_loader.types.book import BookMeta


@dataclass
class RanobelibLoaderOptions:
    book_name: str
    since: int | None = None
    to: int | None = None


@dataclass
class RanobelibChapter:
    number: int
    volume: int
    branch_id: int
    title: str


class RanobelibLoader(BookLoader):
    url: ClassVar[str] = "https://api.cdnlibs.org/api/manga"

    def __init__(
        self,
        options: RanobelibLoaderOptions,
    ) -> None:
        self._options = options
        self._chapters: list[RanobelibChapter] = []

        session = requests.Session()
        retries = Retry(
            total=4,
            backoff_factor=10,
            status_forcelist=[429],
            allowed_methods=["GET"],
        )
        adapter = HTTPAdapter(max_retries=retries)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        self._session = session

    def fetch_meta(self) -> BookMeta:
        response = self._session.get(
            f"{RanobelibLoader.url}/{self._options.book_name}",
            params=(
                ("fields[]", "summary"),
                ("fields[]", "authors"),
                ("fields[]", "otherNames"),
            ),
            timeout=5,
            headers={"Site-Id": "3"},
        )
        response.raise_for_status()
        response_json = response.json()
        return BookMeta(
            authors=[author["name"] for author in response_json["data"]["authors"]],
            name=response_json["data"]["rus_name"],
            description=response_json["data"]["summary"],
            alternative_names=response_json["data"].get("otherNames", None),
        )

    def fetch_content(self) -> Iterable[BookElement]:
        self._init_chapters()
        chapter_elements = []

        for chapter in self._chapters:
            logging.info(
                "load chapter %s, том %s, глава %s",
                chapter.title,
                chapter.volume,
                chapter.number,
            )

            response = self._session.get(
                RanobelibLoader.url + "/" + self._options.book_name + "/chapter",
                json={
                    "volume": chapter.volume,
                    "branch_id": chapter.branch_id,
                    "number": chapter.number,
                },
                timeout=5,
            )
            response.raise_for_status()

            elements: list[BookElement] = []
            try:
                self._parse_content(response.json()["data"]["content"], elements)
                chapter_elements.append(ChapterElement(chapter.title, elements))
            except Exception as e:
                print(e)
                print(response.text)
                raise e

        return chapter_elements

    def _init_chapters(self) -> None:
        response = requests.get(
            RanobelibLoader.url + "/" + self._options.book_name + "/chapters",
            timeout=5,
        )
        chapters = response.json()["data"]

        since = self._options.since

        if since is None:
            since = 0

        to = self._options.to

        if to is None:
            to = len(chapters)

        for chapter in chapters[since : to + 1]:
            branch_id: int = chapter["branches"][0]["id"]
            self._chapters.append(
                RanobelibChapter(
                    number=chapter["number"],
                    volume=chapter["volume"],
                    branch_id=branch_id,
                    title=chapter["name"],
                )
            )

    def _parse_content(self, content: Any, elements: list[BookElement]) -> None:  # noqa: ANN401
        if isinstance(content, list):
            for i in content:
                self._parse_content(i, elements)
        elif isinstance(content, str):
            ...
        else:
            if content["type"] == "paragraph" or content["type"] == "doc":
                if "content" in content:
                    self._parse_content(content["content"], elements)
            if content["type"] == "text":
                elements.append(ParagraphElement(content["text"]))
