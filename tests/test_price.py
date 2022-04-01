import pytest
from lark import Lark
from lark.exceptions import UnexpectedInput

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
        "2022-03-31 price BTC 12.34 USD",
        "2022-03-31 price BTC 12.34 USD ; this is a comment",
    ],
)
def test_parse_price(price_parser: Lark, text: str):
    price_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    [
        "price USD 12.34 USD",
        "2022-03-1 price Assets:Bank 12.34 USD",
        "2022-03 price BTC 12.34 USD",
        "2022-03-01 price BTC 12.34",
    ],
)
def test_parse_bad_price(price_parser: Lark, text: str):
    with pytest.raises(UnexpectedInput):
        price_parser.parse(text)
