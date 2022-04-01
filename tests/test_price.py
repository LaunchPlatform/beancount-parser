import pytest
from lark import Lark
from lark.exceptions import UnexpectedCharacters

from beancount_parser.parser import GRAMMAR_FOLDER


@pytest.fixture
def price_parser() -> Lark:
    return Lark(
        """
    start: price
    %import .price.price
    %ignore " "
    """,
        import_paths=[GRAMMAR_FOLDER],
    )


@pytest.mark.parametrize(
    "text",
    [
        "@ 12.34 USD",
        "@@ 12.34 USD",
    ],
)
def test_parse_price(price_parser: Lark, text: str):
    price_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    [
        "12.34 USD",
    ],
)
def test_parse_bad_price(price_parser: Lark, text: str):
    with pytest.raises(UnexpectedCharacters):
        price_parser.parse(text)
