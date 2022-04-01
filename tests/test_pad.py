import pytest
from lark import Lark
from lark.exceptions import UnexpectedInput

from beancount_parser.parser import GRAMMAR_FOLDER


@pytest.fixture
def pad_parser() -> Lark:
    return Lark(
        """
    start: pad
    %import .pad.pad
    %ignore " "
    """,
        import_paths=[GRAMMAR_FOLDER],
    )


@pytest.mark.parametrize(
    "text",
    [
        "2022-03-31 pad Assets Expenses",
        "2022-03-31 pad Assets:Bank Expenses ; this is a comment",
    ],
)
def test_parse_pad(pad_parser: Lark, text: str):
    pad_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    [
        "pad Assets",
        "2022-03-1 pad Assets:Bank",
        "2022-03 pad Assets:Bank USD",
        "2022-03-31 pad Assets:Bank 123",
        '2022-03-31 pad USD,BTC "STRICT"',
        '2022-03-31 pad Foobar USD,BTC "NONE"',
    ],
)
def test_parse_bad_pad(pad_parser: Lark, text: str):
    with pytest.raises(UnexpectedInput):
        pad_parser.parse(text)
