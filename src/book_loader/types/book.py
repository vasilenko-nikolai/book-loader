from dataclasses import dataclass


@dataclass(frozen=True)
class BookMeta:
    authors: list[str] | None = None
    description: str | None = None
    name: str | None = None
    alternative_names: list[str] | None = None
    genres: list[str] | None = None
    translators: list[str] | None = None
