import logging

from book_loader.formatters.txt import TxtFormatter
from book_loader.loaders import ranobelib

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    loader = ranobelib.RanobelibLoader(
        ranobelib.RanobelibLoaderOptions(
            book_name="165329--kusuriya-no-hitorigoto-ln-novel",
            since=0,
            to=30,
        )
    )

    elements = loader.load()

    txt_bytes = TxtFormatter().format(elements)

    with open("book.txt", "wb") as f:
        f.write(txt_bytes)
