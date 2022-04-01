from textwrap import dedent

import pytest
from lark import Lark
from lark.exceptions import UnexpectedInput

from beancount_parser.parser import GRAMMAR_FOLDER


@pytest.fixture
def balance_parser() -> Lark:
    return Lark(
        """
    start: balance
    %import .balance.balance
    %ignore " "
    """,
        import_paths=[GRAMMAR_FOLDER],
    )


@pytest.mark.parametrize(
    "text",
    [
        "2022-03-31 balance Assets 12.34 USD",
        "2022-03-31 balance Assets:Bank 45.67 BTC",
        "2022-03-31 balance Assets:Bank 45.67 BTC ; this is a comment",
        dedent(
            """\
        2022-03-31 balance Assets 12.34 USD
            foo: "bar"
            egg: #spam
        """
        ),
    ],
)
def test_parse_balance(balance_parser: Lark, text: str):
    balance_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    [
        "balance Assets",
        "2022-03-1 balance Assets:Bank",
        "2022-03 balance Assets:Bank USD",
        "2022-03-31 balance Assets:Bank 123",
    ],
)
def test_parse_bad_open(balance_parser: Lark, text: str):
    with pytest.raises(UnexpectedInput):
        balance_parser.parse(text)
