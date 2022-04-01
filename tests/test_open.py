from textwrap import dedent

import pytest
from lark import Lark
from lark.exceptions import UnexpectedInput

from beancount_parser.parser import GRAMMAR_FOLDER


@pytest.fixture
def open_parser() -> Lark:
    return Lark(
        """
    start: open
    %import .open.open
    %ignore " "
    """,
        import_paths=[GRAMMAR_FOLDER],
    )


@pytest.mark.parametrize(
    "text",
    [
        "2022-03-31 open Assets",
        "2022-03-31 open Assets:Bank",
        "2022-03-31 open Assets:Bank USD",
        "2022-03-31 open Assets:Bank USD,BTC",
        '2022-03-31 open Assets:Bank USD,BTC "STRICT"',
        '2022-03-31 open Assets:Bank "STRICT"',
        '2022-03-31 open Assets:Bank USD,BTC "NONE"',
    ],
)
def test_parse_open(open_parser: Lark, text: str):
    open_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    [
        "open Assets",
        "2022-03-1 open Assets:Bank",
        "2022-03 open Assets:Bank USD",
        "2022-03-31 open Assets:Bank 123",
        '2022-03-31 open USD,BTC "STRICT"',
        '2022-03-31 open Foobar USD,BTC "NONE"',
    ],
)
def test_parse_bad_open(open_parser: Lark, text: str):
    with pytest.raises(UnexpectedInput):
        open_parser.parse(text)
