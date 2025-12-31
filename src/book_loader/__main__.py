import logging

from book_loader.formatters.fb2 import Fb2Formatter
from book_loader.loaders import ranobelib

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    loader = ranobelib.RanobelibLoader(
        ranobelib.RanobelibLoaderOptions(
            book_name="165329--kusuriya-no-hitorigoto-ln-novel",
            since=1,
            to=20,
        )
    )

    book_meta = loader.fetch_meta()
    book_elements = loader.fetch_content()

    formatter = Fb2Formatter(book_meta)
    fb2_bytes = formatter.format(book_elements)

    with open("book.fb2", "wb") as f:
        f.write(fb2_bytes)
