import pytest
from lark import Lark
from lark.exceptions import UnexpectedInput

from beancount_parser.parser import GRAMMAR_FOLDER


@pytest.fixture
def amount_parser() -> Lark:
    return Lark(
        """
    start: amount
    %import .amount.amount
    %ignore " "
    """,
        import_paths=[GRAMMAR_FOLDER],
    )


@pytest.mark.parametrize(
    "text",
    [
        "12.34 USD",
        "-12.34 USD",
        "0.0 USD",
        "500 BTC",
    ],
)
def test_parse_amount(amount_parser: Lark, text: str):
    amount_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    [
        "12.34",
        "USD",
        "0..0 USD",
    ],
)
def test_parse_bad_amount(amount_parser: Lark, text: str):
    with pytest.raises(UnexpectedInput):
        amount_parser.parse(text)
